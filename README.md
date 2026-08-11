# ads-b-aircraft-tracker
Summer project using Raspberry Pi 3B+ to learn about signal processing and communication

## Project Plan
- Milestone 1 - Pi Setup and Linux Basics, July 20-23
- Milestone 2 - SDR Setup and Signal Learning, July 24 and July 27-29
- Milestone 3 - Flask Backend, July 30-31 and August 2-3
- Milestone 4 - Frontend Map and GUI, August 4-7 and August 10-11
- Final Polish - August 20-28

## Setup

### Milestone 1 - Pi Setup and Linux Basics, Completed July 24, 2026
- Flashed Raspberry Pi OS (64-bit Desktop) using Raspberry Pi Imager
- Installed heatsink and fan kit (fan connected to GPIO 5V or 3.3V and GND pins)
- Connected and tested GeeekPi 7" touchscreen via HDMI and USB
- Enabled SSH during flashing for remote access
- Set up VS Code Remote-SSH for development from laptop
- Initialized Git repository and connected to GitHub
- Also, virtual memory added to increase to 2.0 GB since the Pi crashed a few times due to dump1090 taking up most of the ram and then VS Code took up the remaining ram (did this during Milestone 3 when it became an issue)

## Installation

### Milestone 2 - SDR Setup and Signal Learning, Completed July 29, 2026
- Installed RTL-SDR driver on Pi - https://www.nooelec.com/store/downloads/dl/file/id/72/product/0/nesdr_installation_manual_for_ubuntu.pdf
- Added the FlightAware apt repository and installed dump1090-fa - Steps 1-4 and 6 of https://www.flightaware.com/adsb/piaware/install
- dump1090-fa runs automatically as a service on boot. To check status: sudo systemctl status dump1090-fa
- Viewed live aircraft data that is written to `/run/dump1090-fa/aircraft.json` and updated every second
- Viewed built-in map at http://[pi-ip]:8080, will make own site using flask and leaflet.js
- Learned about the signal chain, from the antenna to output as readable data

#### Summary of signal chain:
- Antenna receives signal
- Tuner downconverts signal
- ADC samples downconverted signal
- IQ samples sent to software to be process
- (Tuner and ADC are inside USB dongle)
- dump1090 receives IQ samples 
- dump1090 listens for 8 microsecond preamble
- Once hears 8 microsecond preamble reads the 112-bit message that is Pulse Position Modulated (very similar looking to Manchester Encoded messages)
- Does CRC-24 error checking as soon as it decodes message to ensure message sent correctly
- Once CRC-24 error checking is verified, dump1090 outputs the received information
- Received information can then be used or displayed as wanted
- Full signal processing notes: [docs/signal-processing-notes.md](docs/signal-processing-notes.md)

## Backend
### Milestone 3 - Flask Backend, Completed August 3, 2026
- Installed Flask on Pi using virtual environment to only download for this project - https://flask.palletsprojects.com/en/stable/installation/
- Followed Quickstart to learn Flask basics - https://flask.palletsprojects.com/en/stable/quickstart/
- Learned about basics of backend, along with routes and endpoints
- Built a Flask server that reads and filters only needed data from dump1090's JSON output
- Server returns a JSON with aircraft data, will connect frontend to this in next Milestone
- Server accessible at http://[pi-ip]:5000/ returning filtered live aircraft data

## Frontend
### Milestone 4 - Frontend Map and GUI, Completed August 11, 2026
- Learned basics of HTML, CSS, and JavaScript to build the frontend
- Followed Leaflet Quick Start and Custom Icons tutorial to learn basics - https://leafletjs.com/examples/quick-start/ and https://leafletjs.com/examples/custom-icons/
- Built a single page web app served by Flask using Leaflet.js for the live map
- Aircraft displayed as rotatable SVG plane icons using a B737 path from 
  https://github.com/RexKramer1/AircraftShapesSVG
- Aircraft markers tracked by ICAO hex code and updated in place each second 
  rather than redrawn, preserves popups and details panel
- Markers removed after 60 seconds with no new signal, matching dump1090-fa's 
  own timeout
- Click any aircraft to open a details panel showing flight number, ICAO hex, 
  altitude (m), speed (km/h), heading, latitude, longitude, squawk code, 
  emergency status, and RSSI
- Toggle between map view and list view showing all currently tracked aircraft
- RSSI displayed in both details panel and list view
- Map fills the full screen with fixed toggle buttons and shutdown button overlaid
- Shutdown button in bottom left corner safely stops dump1090-fa and powers 
  down the Pi