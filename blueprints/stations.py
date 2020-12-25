from flask import Blueprint, jsonify

from services import firestore

stations_bp = Blueprint('stations_bp', __name__, )


@stations_bp.route('')
def get_all():
    stations = firestore.read_all('stations')
    return jsonify(stations)
