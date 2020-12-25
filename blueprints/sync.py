import time
import gc
from flask import Blueprint, request
import requests
import zipfile
import xml.etree.ElementTree as ET
import os
from google.cloud import tasks_v2
from config import XML_URL, PROJECT_ID, TASK_QUEUE, ZONE
from services import firestore

sync_bp = Blueprint('sync_bp', __name__, )


@sync_bp.route('')
def sync():
    # Create a client.
    client = tasks_v2.CloudTasksClient()

    # Construct the fully qualified queue name.
    parent = client.queue_path(PROJECT_ID, ZONE, TASK_QUEUE)

    # Construct the request body.
    task = {
        'app_engine_http_request': {  # Specify the type of request.
            'http_method': tasks_v2.HttpMethod.GET,
            'relative_uri': '/api/sync/start'
        }
    }

    # Use the client to build and send the task.
    response = client.create_task(parent=parent, task=task)

    print('Created task {}'.format(response.name))
    return "ok"


@sync_bp.route('/start')
def start():
    idx_number = request.args.get('idx')
    time1 = time.time()
    download_url('/tmp/data.zip')
    print("zip file downloaded")

    extract_zip('/tmp/data.zip', '/tmp')
    print("zip file extracted")

    os.remove('/tmp/data.zip')
    print("zip file deleted")

    stations = read_xml('/tmp/PrixCarburants_instantane.xml')
    print(f"{len(stations)} fetched")

    for idx, station in enumerate(stations):
        if idx_number and idx < idx_number:
            continue
        time_tmp = time.time()
        if time_tmp - time1 > 540:
            client = tasks_v2.CloudTasksClient()
            parent = client.queue_path(PROJECT_ID, ZONE, TASK_QUEUE)
            task = {
                'app_engine_http_request': {  # Specify the type of request.
                    'http_method': tasks_v2.HttpMethod.GET,
                    'relative_uri': '/api/sync/start?idx=' + str(idx)
                }
            }
            response = client.create_task(parent=parent, task=task)
            print("took too much time, created a new task")
            break
        firestore.add('stations', station, station['id'])
        print(f"{idx + 1} out of {len(stations)}")

    time2 = time.time()
    print('function took %0.3f s' % (time2 - time1))
    return "done"


def download_url(save_path, chunk_size=128):
    r = requests.get(XML_URL, stream=True)
    with open(save_path, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=chunk_size):
            fd.write(chunk)
        fd.close()
    gc.collect()


def extract_zip(path_to_zip_file, directory_to_extract_to):
    with zipfile.ZipFile(path_to_zip_file, 'r') as zip_ref:
        zip_ref.extractall(directory_to_extract_to)
        zip_ref.close()
    gc.collect()


def read_xml(path_to_file):
    root = ET.parse(path_to_file).getroot()
    gc.collect()
    stations = []
    for pdv in root.findall('pdv'):
        station = {
            "cp": pdv.get('cp'),
            "id": pdv.get('id'),
            "latitude": float(add_char(pdv.get('latitude'), '.', 2)),
            "longitude": float(add_char(pdv.get('longitude'), '.', 1)),
            "adresse": pdv.find('adresse').text,
            "ville": pdv.find('ville').text,
            "prix": [],
            "horaires": [],
            "services": [],
        }

        for service in pdv.findall('services/service'):
            station['services'].append(service.text)

        for price in pdv.findall('prix'):
            station['prix'].append({
                "nom": price.get('nom'),
                "id": price.get('id'),
                "maj": price.get('maj'),
                "valeur": price.get('valeur'),
            })

        horaires = pdv.find('horaires')

        if not horaires:
            stations.append(station)
            continue

        if horaires.get('automate-24-24') == '1':
            station['horaires'] = None
        else:
            jours = horaires.findall('jour')
            for day in jours:
                try:
                    station['horaires'].append({
                        "jour": day.get('nom'),
                        "ferme": day.get('ferme') == '1',
                        "id": day.get('id'),
                        "ouverture": day.find('horaire').get('ouverture'),
                        "fermeture": day.find('horaire').get('fermeture'),
                    })
                except AttributeError as e:
                    break
        stations.append(station)
    return stations


def add_char(text, char, place):
    text = text.replace('.', '')
    return text[:place] + char + text[place:]


