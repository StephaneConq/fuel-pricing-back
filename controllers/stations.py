import json
import time
from controllers.state_api import fetch_stations
from models.station import Station
from utils.db import DBUtil


def sync():
    db_utils = DBUtil()
    db_utils.delete_all("stations")

    start = 0
    nb_rows = 100
    stations = []
    start_time = time.time()
    cpt = 0

    while True:
        res = fetch_stations(nb_rows=nb_rows, start=start)

        if res.get("nhits") == 0:
            print("weird no result fetched, retrying")
            continue

        stations = list(map(format_station, res.get("records", [])))
        sql_stations = list(map(lambda s: Station(**s), stations))
        db_utils.bulk_save(sql_stations)

        cpt += len(stations)
        print(f"updated {cpt} rows out of {res.get('nhits')}")
        if len(stations) < nb_rows:
            break
        else:
            start += len(stations)

    print(f"time enlapsed : {time.time() - start_time} seconds")


def format_station(station):
    prices = json.loads(station.get("fields").get("prix", "[]"))
    if type(prices) == dict:
        prices = [prices]
    else:
        for p in prices:
            p["@valeur"] = float(p.get("@valeur", 0))
    horaires = json.loads(station.get("fields").get("horaires", "[]"))
    if type(horaires) == dict:
        if horaires.get("@automate-24-24", "0") == "1":
            horaires["@automate-24-24"] = True
        else:
            horaires["@automate-24-24"] = False
    return {
        "lat": station.get("fields").get("geom")[0],
        "lng": station.get("fields").get("geom")[1],
        "adresse": station.get("fields").get("adresse"),
        "region": station.get("fields").get("region"),
        "departement": station.get("fields").get("departement"),
        "ville": station.get("fields").get("ville"),
        "code_departement": station.get("fields").get("code_departement"),
        "prix": prices,
        "id": station.get("fields").get("id"),
        "horaires": json.loads(station.get("fields").get("horaires", "[]")),
    }


def list_stations(bounds=None):
    db_utils = DBUtil()
    if bounds is None:
        return db_utils.list_all(Station)
    stations = (
        db_utils.session.query(Station)
        .filter(Station.lat < bounds.get("left").get("lat"))
        .filter(Station.lat > bounds.get("right").get("lat"))
        .filter(Station.lng < bounds.get("right").get("lng"))
        .filter(Station.lng > bounds.get("left").get("lng"))
        .all()
    )
    return list(map(lambda s: s.as_dict(), stations))
