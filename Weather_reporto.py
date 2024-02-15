import datetime as dt
import json

import requests
from flask import Flask, jsonify, request

API_TOKEN = ""

app = Flask(__name__)


class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv["message"] = self.message
        return rv


def get_weather(location, date):

    url_base = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline"
    location = str(location)
    date = str(date)
    key = ""
    url = f"{url_base}/{location}/{date}?unitGroup=metric&include=days&key={key}&contentType=json"

    response = requests.get(url)

    if response.status_code == requests.codes.ok:
        return json.loads(response.text)
    else:
        raise InvalidUsage(response.text, status_code=response.status_code)


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.route("/")
def home_page():
    return "<p><h2>Weather forecast</h2></p>"


@app.route("/weatherforecast", methods=["POST"])
def weather_report():
    json_data = request.get_json()

    token = json_data.get("token")
    name = json_data.get("requester_name")
    date = json_data.get("date")
    location = json_data.get("location")

    if token is None:
        raise InvalidUsage("token is required", status_code=400)
    if location is None:
        raise InvalidUsage("no location given", status_code=400)
    if date is None:
        date = dt.datetime.today().date()
    if name is None:
        name = "anonymous"

    if token != API_TOKEN:
        raise InvalidUsage("wrong API token", status_code=403)

    
    weather_full = get_weather(location, date)
    location = weather_full['resolvedAddress']
    weather = weather_full["days"][0]
    date = weather["datetime"]


    end_time = dt.datetime.now().isoformat(timespec='seconds')
    end_time = str(end_time)+"Z"

    result = {
        "requester_name": name,
        "timestamp": end_time,
        "location": location,
        "date": date,
        "weather": {
            "overall":weather["description"],
            "temp(C)":weather["temp"],
            "temp_feelslike(C)":weather["feelslike"],
            "wind(kmph)":weather["windspeed"],
            "humidity(%)":weather["humidity"]
        }
    }

    return result
