# imports
from flask import Flask, jsonify
import json

# create a Flask app instance
app = Flask(__name__)

# route for data
@app.route("/")
def get_aircraft_data():
    # call function to filter data
    filtered_data = filter_aircraft_data()
    return jsonify(filtered_data)

# function to filter data to only wanted information
def filter_aircraft_data():
    # read JSON data from file, get as dictionary
    with open("/run/dump1090-fa/aircraft.json", "r") as file:
        json_data = json.load(file)

    # create empty dictionary for filtered data
    filtered_data = {}

    # keys to extract
    wanted_keys = ["hex", "flight", "alt_baro", "gs", "track", "squawk", "emergency", "lat", "lon", "seen_pos", "seen"]

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

    # print number of aircraft in filtered data
    for key in filtered_data:
        if key == "aircraft":
            number_of_aircraft = len(filtered_data[key])
            print(f"Number of aircraft: {number_of_aircraft}")
    
    return filtered_data

# run the app when this file is executed directly
if __name__ == "__main__":
    app.run(host = "0.0.0.0", debug = True)