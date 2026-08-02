# imports
from flask import Flask
import json

# create a Flask app instance
app = Flask(__name__)

# route for data
@app.route("/")
def get_aircraft_data():
    with open("/run/dump1090-fa/aircraft.json", "r") as file:
        data = json.load(file)
    return data

# run the app when this file is executed directly
if __name__ == "__main__":
    app.run(debug=True)