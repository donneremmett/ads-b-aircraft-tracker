## Milestone 2:
### Antenna Information:
- https://strykerradios.com/ham-radios/ham-radio-antenna-types-differences-pros-cons/
- Need to use length specifically based on what trying to get, for aircraft it is 1090MHz
- Radio waves are vertically polarized so the antenna needs to be pointing upwards
- If length is wrong the waves will still hit the antenna, just the signal strength will be significantly degraded and may be too weak to be analyzed
 
- Antenna Length Calculation
- c = lambda * f, so lambda = c/f
- Increasing wanted frequency decreases required antenna length
- Wavelength = c (speed of light - 3x10^8 m/s) / f (frequency wanted)
- ADS-B is broadcast at 1090 MHz
- Wavelength = 3x10^8 m/s / 1090x10^6 Hz (or 1/s)
- Wavelength = 0.2752 m or 27.52 cm
- In air radio waves travel at 100% speed of light, while in metal travels at approx 95% speed of light
- Wavelength travelling through metal = 27.52 cm * 0.95
- Wavelength travelling through metal = 26.15 cm
 
- However, since the impedance of the antenna must match the impedance of RTL-SDR dongle, using quarter wave length is much more appropriate and allows radio wave energy to slide into RTL-SDR dongle. At full length the impedance of the antenna is much higher - leading to lots of radio waves being deflected, rather than received by RTL-SDR dongle.
- Because of this, use quarter wavelength of half wavelength for the antenna
- Also if a metal piece is put under the antenna, it acts as a ground plane, reflecting the wave, effectively doubling the strength of the signal. Metal needs to go out by at least a quarter of a wavelength to be useful. Also the ground plane focuses the antenna on the horizon, where aircraft are.
 
- Quarter wave antenna length = 26.15 cm / 4
- Quarter wave antenna length = 6.53 cm
 
- Half wave antenna length = 26.15 cm / 2
- Half wave antenna length = 13.07 cm
 
- Will use 13.07 cm length, actually 13.5 cm is smallest antenna can go
- Will put piece of metal with radius of at least 6.5 cm underneath for ground plane

### Latitude and Longitude:
- Latitude - distance north or south of equator, horizontal lines
- Longitude - distance east or west of Prime Meridian (Greenwich, London, England), vertical lines

- Latitude, then longitude always
- Reported as Degrees, Minutes, Seconds (DMS) or Decimal Degrees
- For Decimal Degrees North and East are positive, South and West are negative

### dump1090 JSON File Outputs Explained:
- dump1090-fa starts automatically when pi is turned on
- https://github.com/edgeofspace/dump1090-fa/blob/master/README-json.md
- aircraft.json uses decimal degrees for lat and lon
- Will use lat, lon, hex (ICAO address), seen, seen_pos, track (angle for positioning), flight, alt_baro, gs, squawk, emergency
 
### Noise Floor: 
- https://en.wikipedia.org/wiki/Noise_floor
- Noise - any signal other than one being monitored, many different types
- Thermal noise, internal receiver noise, and external/atmospheric receiver noise all contribute to the noise floor of a receiver
- Noise floor - minimum signal level that a receiver can detect
- Measure of signal created from sum of all noise sources and unwanted signals 
- Baseline level of random electrical noise that exists in any receiver
- Lower noise floor by cooling system to reduce thermal noise or artificially lower it using digital signal processing
- In general a radio signal must be stronger than noise floor to be heard and processed correctly

### Signal to Noise Ratio (SNR): 
- https://en.wikipedia.org/wiki/Signal-to-noise_ratio
- Compares (as a ratio) power of desired signal to power of background noise
- Usually in decibels (dB), different equations using logarithms for SNR
- Ratio higher than 1:1 is more signal than noise
- Higher ratio means more useful signal than unwanted static or interference, cleaner and clearer output
- High SNR - signal is clear and easy to detect and interpret
- Low SNR - signal is corrupted or obscured by noise, difficult to distinguish or recover
- Increasing distance from transmitter drops the signal off according to inverse square law
- Improve SNR by increasing signal strength, reducing noise level, filtering out unwanted noise or using error correction
- SNR determines max amount of data that can be transmitted reliably over a given channel and how far away aircraft can be to still receive their signals
 
- When put antenna under bed or not by window, both increase the noise floor and decrease strength of received signal, making it harder to interpret farther away aircraft
 
### IQ Sampling Revisited:
- Sample period - measured in T seconds, amount of time in between samples
- Sample rate - measured in Hz, 1/T, amount of samples taken per second
- Nyquist rate - minimum rate can sample at to accurately determine the signal, is double the highest frequency component
- Aliasing - get if don’t sample fast enough
- IQ Sampling - get IQ sample which is a complex number representing the amplitudes of a cos and sin wave respectively
- Measuring two parts of a signal at a 90-degree angle apart
- Lets receivers process wide frequency bands using lower sample rates
- Incoming signal radio signal is multiplied by two reference signals (cos for I and sin for Q)
- I is in phase, amplitude of cos
- Q is quadrature, 90 degrees out of phase, amplitude of sin
- Can get original signal from the IQ samples

### Manchester Encoding: 
- https://en.wikipedia.org/wiki/Manchester_code
- Encoding - process of turning data or message into a signal
- Bit - smallest unit of digital information, 1 or 0
- Used for data transmission where the sender and receiver must stay synchronized without a separate clock wire
- Instead of using steady voltage levels to send 1s and 0s for a signal, it is a digital method using voltage changes to transmit data
- Has mid-bit transition for every single bit that makes the signal self-clocking
- Combines data and clock signals into a single self-synchronizing stream
- Every bit time is cut into equal halves, with the voltage always changing right in the middle of the bit
- Representing a 1 - signal goes from high to low voltage in middle (falling edge)
- Representing a 0 - signal goes from low to high voltage in middle (rising edge)

- Used because it is self-clocking so don’t need a separate clock wire
- Also has no DC voltage build up due to signal spending an equal amount of time high and low, so signal passes easily through transformers or capacitors
- Manchester encoding uses more bandwidth since each bit requires two distinct signal levels (up and down), so takes twice as much bandwidth to send same amount of data
- Manchester encoding is the method used to physically transmit aircraft data through the air at 1090 MHz
- https://www.aopa.org/go-fly/aircraft-and-ownership/ads-b/ads-b-glossary
- ADS-B transponders use 1090ES (Mode S Extended Squitter - periodic and unprompted, squitter means it automatically broadcasts regardless of being requested, hence automatic in ADS-B) standard, data rate of 1 Megabit per second, so every bit takes exactly 1  microsecond to transmit
- Because Manchester encoding is used each bit is split into two 0.5 microsecond halves
- ADS-B uses Manchester encoding because there is no shared clock wire
- Dump1090 has functions to handle Manchester encoding but basically samples the radio signal at a high rate and check every 1  microsecond how the first half microsecond power compares to the second half microsecond power
- If both halves are equal then the software knows the signal suffered from collision or interference and discards the corrupted packet

### ADS-B Preamble Detection: 
- Used to spot start of incoming aircraft radio signal
- Listens for specific pattern of four short radio pulses in first 8 microseconds, each pulse lasts 0.5 microseconds
- Preamble does not use Manchester encoding
- Comes before the aircraft sends its GPS position and flight details
- Send four quick pulses at exact intervals of 0, 1.0, 3.5, and 4.5 microseconds, which is unique so receiver knows to ignore random  static and noise
- Final three seconds are completely silent to allow receiver slight bit of time to stabilize before the fast Manchester data stream begins
- Real aircraft data comes after
- Preamble is used to alert receiver that a ADS-B packet is arriving
Detects this preamble using peak and valley detection to ensure that the peaks and valleys are due to the signal and not background - noise

### Pulse Position Modulation (PPM): 
- https://en.wikipedia.org/wiki/Pulse-position_modulation
- Signal encoding method where amplitude and width of pulses stay constant while timing position shifts
- Distance or delay of pulse shift matches value of input sample data
- After preamble, the SDR starts recording the 112 microseconds (corresponding to 112 bits of data since 1090ES has bit rate of 1Mbps)
- Software decodes the PPM pretty much identically to Manchester Encoding
- Technically ADS-B uses PPM (position of pulse in a timed slot) which is a version of Manchester Encoding (has transition in middle)
- Bits 9-32 - ICAO 24-bit address
- Bits 33-88 - other aircraft data
- Bits 89-112 - CRC-24
 
### CRC-24 Error Checking: 
- https://en.wikipedia.org/wiki/Cyclic_redundancy_check and https://mode-s.org/1090mhz/content/ads-b/- 8-error-control.html
- CRC stands for Cyclic Redundancy Check 
- CRC-24 is 24-bit error-checking code to verify if data was changed of damaged during transmission
- Uses binary division and specific 24-bit remainder
- Treats message as a binary number and divides it by a fixed standard number
- Then attaches the remainder to end of data
- For CRC-24 generator polynomial (that sender and receiver agree on) is 25 bits long to create a 24-bit remainder
- Sender divides data bits of the message plus 24 bits of zeros by the key using binary long division
- 24-bit remainder from this division is the CRC checksum
- Sender attaches these 24 bits to original message (replace 24-bits of zeroes) and sends them with the message
- Receiver takes incoming message and attached 24-bit CRC value
- Does exact same division using the key (except now the message already has the perfect remainder at end, making it perfectly divisible by the key)
- If final remainder is all zeros then the data arrived safely
- If remainder is anything other than zero then the data was corrupted in transit, so the data is rejected and/or re-requested
- For Mode S (aircraft that have older non ADS-B and do not transmit location so do not show up map), CRC-24 is modified to use bit-clearing to double-check the aircraft’s identity
- Bit-clearing is where the ICAO address (24-bit aircraft id) is mixed into the CRC-24 checksum 
- Mixed using XORs (exclusive or where cannot have both be 1)
- This means the remainder for the receiver will not be zero, but rather the remainder is the exact 24-bit ICAO address of the aircraft
- This address is then verified against a known database of aircraft to ensure it is a real aircraft
- Not including the ICAO address in the checksum is safer as it prevents morphed messages and ICAO addresses
- CRC-24 ensures that the flight data decoded from radio signals is accurate and not corrupted by background noise or signal interference
- After picking up an aircraft’s signal, dump1090 immediately does the CRC-24 division
- Aircraft data only output from dump1090 if remainder is zero
- Used to discard corrupted packets if remainder on receiver end is not correct

### Frequency Downconversion: 
- Shifting electronic signal from high frequency to lower more manageable frequency 
- Use a mixer and local oscillator to make weak signals easier to filter, amplify and process
- High frequency radio wave is captured by antenna and sent to receiver system
- Local oscillator generates steady internal frequency and mixer multiples incoming signal with local oscillator signal
- Multiplying creates two new frequencies - one at sum of frequencies and one at difference
- Filter then blocks high sum frequency and keeps lower difference frequency, is the intermediate frequency that is used for further data processing
- Need to do because lower frequencies allow for easier filtering, better stability, and data is preserved even at lower frequencies
- Inside USB dongle:
- R820T2 is tuner that receives signal, amplifies specific frequency wanted, and then downconverts the frequency to be used
- RTL2832U is an analog to digital converter (ADC), receives the downconverted signal and converts it into digital 1s and 0s specifically into raw digital IQ samples, which are then sent through the USB to be processed by software

- Need to downconvert using the tuner so that ADC can sample fast enough (at least twice as fast as frequency) to capture the signal  accurately
- Tuner downconverts the signal to slow it down to a low intermediate frequency 
- Using downconversion also makes filtering background noise easier and prevents signal loss
- Is the trick to allow a cheap USB dongle to do same work as an expensive laboratory receiver, since ADC cannot sample fast enough for 1090 MHz (would need to sample at least at 2180 MHz)

### Summary of Signal’s Process: 
- Antenna receives signal
- Tuner downconverts signal
- ADC samples downconverted signal
- IQ samples sent to software to be processed
- (Tuner and ADC are inside USB dongle)
- dump1090 receives IQ samples 
- dump1090 listens for 8 microsecond preamble
- Once hears 8 microsecond preamble reads the 112-bit message that is Pulse Position Modulated (very similar looking to Manchester Encoded messages)
- Does CRC-24 error checking as soon as it decodes message to ensure message sent correctly
- Once CRC-24 error checking is verified, dump1090 outputs the received information
- Received information can then be used or displayed as wanted

## Milestone 4:
### Signal Strength (RSSI) - Received Signal Strength Indicator:
- Measures power level of received radio signal
- In negative decibel-milliwatts, numbers closer to zero mean a stronger signal, zero is the baseline/reference/absolute ceiling
- In general:
- -30 to -50 dBm is max signal
- -60 to -67 dBm is good reliable signal
- -70 dBm to -80 dBm is fair to weak signal
- Below -86 dBm is extremely poor signal
- RSSI measures the total received power, including noise
- For this project the higher the RSSI value, the closer the aircraft is to my antenna or there is a direct and unblocked line of sight between aircraft and antenna
- dump1090-fa uses dBFS instead of dBm
- dBFS is decibels relative to full scale
- 0 dBFS is absolute max, highest digital value SDR’s ADC can handle
- Cannot convert to dBm since dBFS is relative
- For dBFS:
- 0 to -3 dBFS is a signal that is too strong and can overload the tuner
- -5 to -15 dBFS is a strong signal
- -20 to -40 dBFS is a good signal
- -45 dBFS is close to noise floor, so signal too weak to decode

### Data Latency:
- Time delay between when data is created/requested/sent and when it is received/processed/made usable
- Delay is caused due to physical distance, processing, network congestion, and hardware limits (like slow storage or CPU throttling)
- Delay between aircraft transmitting its data and marker updating in my tracker is called end to end latency
- For this project there is a delay between aircraft transmitting its data and my map updating as the signal has to travel through the air (at the speed of light), reach the antenna, be downconverted by the tuner and go through the ADC in the dongle, be processed by dump1090, read by the server, and updated on the frontend on the map
- Server is polled once every second (since dump1090 updates once every second), so this adds an additional one second of latency
- Overall one to two seconds of end to end latency at best for this

### Dropout and Data Loss:
- Dropout - sudden temporary loss of signal or data packets due to transmission errors, sensor failures, or overflows
- Creates missing values and gaps in data
- For this project dropouts can occur when a signal is not fully received by the antenna, when dump1090 does not output corresponding data, when the map marker does not update and stays frozen, and if the ADC becomes overloaded by a very strong signal
- Basically dropout can occur often when receiving signals, so my tracker keeps tracking old aircraft and deletes them if a new signal has not been received from it after 60 seconds
- I chose 60 seconds since that is the same amount of time that dump1090-fa uses before deleting old aircraft that have not received another signal
