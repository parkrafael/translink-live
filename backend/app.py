from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from google.transit import gtfs_realtime_pb2
import requests
import os

load_dotenv()
API_KEY = os.getenv('API_KEY')

app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    return request_translink_api()

def request_translink_api():
    response = requests.get(f'https://gtfsapi.translink.ca/v3/gtfsposition?apikey={API_KEY}')
    feed = gtfs_realtime_pb2.FeedMessage()
    feed.ParseFromString(response.content)

    vehicles = []
    for entity in feed.entity:
        vehicle = entity.vehicle
        vehicle_simplified = {
            'trip_id': int(vehicle.trip.trip_id),
            'route_id': int(vehicle.trip.route_id),
            'direction_id': int(vehicle.trip.direction_id),
            'vehicle_id': int(vehicle.vehicle.id),
            'position_longitude': int(vehicle.position.longitude),
            'position_latitude': int(vehicle.position.latitude)
        }
        vehicles.append(vehicle_simplified)

    return vehicles