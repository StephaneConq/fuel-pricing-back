import requests
import os


def fetch_stations(nb_rows, start):
    req = requests.get(
        os.environ.get("STATIONS_URL").format(start=start, nb_rows=nb_rows)
    )
    return req.json()
