# ads-b-aircraft-tracker
Summer project using Raspberry Pi 3B+ to learn about signal processing and communication

## Project Plan
- Milestone 1 - Pi Setup and Linux Basics, July 20-23
- Milestone 2 - SDR Setup and Signal Learning, July 24 and July 27-29
- Milestone 3 - Flask Backend, July 30-31 and August 3-4
- Milestone 4 - Fronted Map and GUI, August 5-7 and August 10-11
- Final Polish - August 20-28

## Setup

### Milestone 1 - Pi Setup and Linux Basics 
### Completed July 24, 2026
- Flashed Raspberry Pi OS (64-bit Desktop) using Raspberry Pi Imager
- Installed heatsink and fan kit (fan connected to GPIO 5V or 3.3V and GND pins)
- Connected and tested GeeekPi 7" touchscreen via HDMI and USB
- Enabled SSH during flashing for remote access
- Set up VS Code Remote-SSH for development from laptop
- Initialized Git repository and connected to GitHub

## Installation

### RTL-SDR and dump1090-fa
- Installed RTL-SDR driver on Pi - https://www.nooelec.com/store/downloads/dl/file/id/72/product/0/nesdr_installation_manual_for_ubuntu.pdf
- Added the FlightAware apt repository and installed dump1090-fa - Steps 1-4 and 6 of https://www.flightaware.com/adsb/piaware/install
- dump1090-fa runs automatically as a service on boot. To check status: sudo systemctl status dump1090-fa
- Viewed live aircraft data that is written to `/run/dump1090-fa/aircraft.json` and updated every second
- Viewed built-in map at http://[pi-ip]:8080, will make own site using flask and leaflet.js
- Learned about the signal chain, from the antenna to output as readable data
- Summary of signal chain:
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