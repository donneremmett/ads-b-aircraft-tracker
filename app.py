# imports
from flask import Flask, jsonify, render_template
import json
import time
import subprocess

# create a Flask app instance
app = Flask(__name__)

# route for data
@app.route("/data")
def get_aircraft_data():
    # call function to filter data
    return jsonify(filter_aircraft_data())

# function to filter data to only wanted information
def filter_aircraft_data():
    # read JSON data from file, get as dictionary
    with open("/run/dump1090-fa/aircraft.json", "r") as file:
        json_data = json.load(file)

    # create empty dictionary for filtered data
    filtered_data = {}

    # keys to extract
    wanted_keys = ["hex", "flight", "alt_baro", "gs", "track", "squawk", "emergency", "lat", "lon", "rssi"]

    # go through now, messages, and aircraft keys
    for key in json_data:
        # if aircraft key, go through each aircraft and extract wanted keys
        if key == "aircraft":
            # create empty list for all aircraft data
            filtered_data[key] = []

            # go through each aircraft individually
            for aircraft in json_data[key]:
                # create empty dictionary for this aircraft's data
                aircraft_data = {}

                # go through each wanted key
                for wanted_key in wanted_keys:
                    # add data to aircraft_data dictionary if its key exists
                    if wanted_key in aircraft:
                        aircraft_data[wanted_key] = aircraft[wanted_key]

                    # if key does not exist add None to aircraft_data dictionary
                    # replace with continue if decide do not want to include missing keys
                    else:
                        aircraft_data[wanted_key] = None
                
                # add aircraft_data to filtered_data dictionary under the list for the "aircraft" key
                filtered_data[key].append(aircraft_data)
        
        # if now or messages key, add to filtered data
        else:
            filtered_data[key] = json_data[key]
              
    return filtered_data

# main route (for map and list view)
@app.route("/")
def index():
    return render_template("index.html")

# rotue for shutting down Pi, using subprocess module because more secure
@app.route("/shutdown", methods=['POST'])
def shutdown_system():
    print("Kiosk Shutdown Request Received. Powering down hardware...")

    # try to execute shutdown command, 200 is ok HTTP status code
    try:
        # stop dump1090 cleanly
        subprocess.run(['sudo', 'systemctl', 'stop', 'dump1090-fa'], check=True)
        print("1. Radio decoder service stopped cleanly.")

        # pause to ensure everything is closed
        time.sleep(2)

        # actually shutdown now
        print("2. Launching hardware poweroff...")
        subprocess.run(['sudo', 'poweroff'], check = True)

        return jsonify({"status": "success", "message": "Shutting down"}), 200

    # if shutdown command fails, return error message, 500 is internal server error HTTP status code
    except subprocess.CalledProcessError as e:
        print(f"Graceful shutdown sequence failed: {e}")
        return jsonify({"status": "error", "message": "Sequence failed"}), 500

# run the app when this file is executed directly
if __name__ == "__main__":
    app.run(host = "0.0.0.0", debug = True)