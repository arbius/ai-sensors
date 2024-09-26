project notes

The RTC DS3231 was set up using setDS3231.py. Run from REPL.

ai3.py reads the time from the ds3231 and the temperature  and humidity 
from the AM2302, also known as DHT22, and if networking a available, will
attempt to post the data to a node server.  The code for the server is server.js
The server writes the data to a file named time.json.
A javascript program, named csv.js, reads the time.json file, creates a csv file named 
dth.csv, and optionally deletes the input file. The csv file is used to import into a spreadsheet for charting.