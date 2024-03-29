from flask import abort, Flask, request
import json
import re

from pathlib import Path
import subprocess

from weather_api.weather_routes import weather

app = Flask(__name__)

app.register_blueprint(weather, url_prefix='/weather')


def emailReader():
    subprocess.run(["python", "emailReader.py"])


print("Starting email reader")
emailReader()


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.get('/get-cases')
def get_cases():
    cases = []  
    p = Path("./incidents")
    for x in p.iterdir():
        if x.is_file() and str(x).endswith(".json"):
            with open(x, "r") as file:
                cases.append(json.load(file))

    return cases


@app.get('/get-case/<case_id>')
def get_case(case_id):
    try:
        with open(f"./incidents/{case_id}.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        abort(404)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
