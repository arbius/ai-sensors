import machine
import time
import json
import urequests
import network
import dht
from machine import Pin
import mynet
import getjson
import os
import dthmain
import config

# Set up network credentials
ssid = "Galaxy A25 5G 6737"
password = "11111111"

# Flag for network connectivity
network_connected = False

# Set up DHT22 sensor
dht_pin = Pin(15, Pin.IN)
dht_sensor = dht.DHT22(dht_pin)


# Initialize a list to store data when network is unavailable
data_buffer = []

# Helper function to upload data via web request
def upload_data(data):
    print('data into upload data')
    print(data)
    # url = "http://maker.ifttt.com/trigger/temperature_humidity_readings/with/key/your_ifttt_key"
    url = "https://maker.ifttt.com/trigger/got_dht/with/key/bI23VhzGk2PGkbLKJ5ZsA7"

    headers = {"Content-Type": "application/json"}
    response = urequests.post(url, headers=headers, data=json.dumps(data))
    print("Data uploaded:", response.text)
    response.close()

# Connect to Wi-Fi network
def connect_wifi():
    global network_connected

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Connecting to Wi-Fi...")
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            pass
    print("Connected to Wi-Fi:", wlan.ifconfig())
    network_connected = True


# Main loop


data_dict = getjson.read_data_from_file()




while True:

    dthmain.connect_wifi()



    # Read temperature and humidity from the sensor

    dht_sensor.measure()
    temperature = dht_sensor.temperature()
    humidity = dht_sensor.humidity()


    # Get the current timestamp
    timestamp = time.mktime(time.localtime())

    # Create a dictionary to store the data
    data = {
        "value1": timestamp,
        "value2": temperature,
        "value3": humidity
    }

    last_sample = data

    # wlan = network.WLAN(network.STA_IF)
    # wlan.config(reconnects=3)



    if data_dict:
        print('we have data_dict')
        print(data_dict)
    else:
        print('no data_dict')

    if config.wlan.isconnected:
        print('network is connected')
    else:
        print('Network is not connected')




    if config.wlan.isconnected() and data_dict:
            print('Uploading data_dict (retrieved from data.json)')
            for count, (key, value) in enumerate(data_dict.items(), start=1):
                print(f"Count: {count}")
                print(f"Key: {key}")
                print(f"Temperature: {value['temperature']}")
                print(f"Humidity: {value['humidity']}")
                print()    

            for key, value in data_dict.items():
                data = {
                    "value1": key,
                    "value2": value['temperature'],
                    "value3": value['humidity']
                }
                upload_data(data)

            print('done uploading from data.json')
            # Delete the existing data.json file
            try:
                os.remove("data.json")
                print("data.json deleted successfully.")
            except OSError as e:
                print(f"Error deleting data.json: {e}")

            # # Create an empty data.json file
            # try:
            #     with open("data.json", "w") as empty_file:
            #         empty_file.write("{}")
            #     print("data.json created as an empty file.")
            # except OSError as e:
            #     print(f"Error creating data.json: {e}")

            data_dict = {}  # Clear the data_dict after uploading

    if config.wlan.isconnected():
        # If network is available, upload the data immediately
        print('upload data')
        print(last_sample)

        upload_data(last_sample)
        # data_buffer.append(data)
        # print("Data stored locally:", data)

    else:
        # If network is unavailable, store the data filesystem
        # data_buffer.append(data)
        print("Data stored locally:", last_sample)

        # Write the JSON data to the file
        # Create a file to store temperature and humidity data
        filename = "data.json"
        file = open(filename, "a")
        print("writing to file")

        file.write(json.dumps(last_sample))
        file.write("\n")
        file.flush()  # Ensure data is written immediately
        file.close()

    # Wait for some time before taking the next reading
    #time.sleep(30)

    print('Going to deep sleep')
    
    machine.deepsleep(600000)
