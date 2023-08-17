from fastapi import APIRouter, FastAPI
from controllers import stations

stations_router = APIRouter()


@stations_router.get("/sync")
def run_sync():
    stations.sync()
    return {"status": "done"}


@stations_router.get("")
def list_stations(
    left_lat: float = None,
    left_lng: float = None,
    right_lat: float = None,
    right_lng: float = None,
):
    bounds = None
    if left_lat and left_lng and right_lat and right_lng:
        bounds = {
            "left": {"lat": left_lat, "lng": left_lng},
            "right": {"lat": right_lat, "lng": right_lng},
        }
    return stations.list_stations(bounds)
