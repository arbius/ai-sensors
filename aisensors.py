import network
import time
from machine import Pin, deepsleep
import dht
import urequests
import ujson
import os
import getDS3231  # Import for your custom getDS3231 function
import connect

# Deep sleep duration in milliseconds (e.g., 60 seconds)
SLEEP_DURATION = 60 * 1000

# File to store unsent data
DATA_FILE = "/latest_readings.json"

# Initialize Wi-Fi connection
def connect_to_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)

    for _ in range(10):  # Wait up to 10 seconds for Wi-Fi connection
        if wlan.isconnected():
            print("Connected to WiFi:", wlan.ifconfig())
            return wlan
        time.sleep(1)
    
    print("Failed to connect to WiFi.")
    return wlan

# Initialize I2C and DS3231 (commented out)
# i2c = I2C(scl=Pin(16), sda=Pin(26))
# rtc = ds3231.DS3231(i2c)

# Initialize DHT22 sensor (DHT22 connected to pin 15)
dht22_sensor = dht.DHT22(Pin(15))

# Get time from DS3231 RTC using getDS3231.do_getDS3231 function
def get_rtc_data():
    try:
        dt = getDS3231.do_getDS3231()
        if dt is not None and len(dt) >= 7:
            # Ensure the returned data is in the expected format
            print(f"RTC Data: Year: {dt[0]}, Month: {dt[1]}, Day: {dt[2]}, Hour: {dt[3]}, Minute: {dt[4]}, Second: {dt[5]}")
            return dt
        else:
            print("Unexpected RTC data format:", dt)
            return (0, 0, 0, 0, 0, 0, 0)  # Return default values
    except Exception as e:
        print("Failed to get RTC data:", e)
        return (0, 0, 0, 0, 0, 0, 0)  # Return default values

# Get temperature and humidity from DHT22
def get_dht22_data():
    try:
        dht22_sensor.measure()  # Trigger a reading
        temperature = dht22_sensor.temperature()  # Get temperature
        humidity = dht22_sensor.humidity()  # Get humidity
        return temperature, humidity
    except Exception as e:
        print("Failed to read from DHT22:", e)
        return None, None

# Send data to the Node.js server
server_url = "http://Insp16.local:3000/time"

def send_data_to_server(data):
    print ("send_data_to_server :", data)
    try:
        response = urequests.post(server_url, json=data)
        print("Server response:", response.text)
        response.close()
        return True  # Successfully sent
    except Exception as e:
        print("Failed to send data:", e)
        return False  # Failed to send

# Save multiple readings to a file
def save_unsent_data(readings):
    try:
        with open(DATA_FILE, "w") as f:
            ujson.dump(readings, f)
        print("Stored unsent data to file.")
    except Exception as e:
        print("Failed to store data:", e)

# Load multiple readings from the file
def load_unsent_data():
    try:
        if DATA_FILE in os.listdir():
            with open(DATA_FILE, "r") as f:
                readings = ujson.load(f)
            print("Loaded unsent data from file.")
            return readings
        else:
            return []
    except Exception as e:
        print("Failed to load data:", e)
        return []

# Delete the file storing unsent data after it's successfully sent
def delete_unsent_data():
    try:
        os.remove(DATA_FILE)
        print("Deleted stored unsent data.")
    except Exception as e:
        print("Failed to delete data:", e)

# Main loop to connect Wi-Fi, send data, and enter deep sleep
def main():
    # Load any unsent data from the previous cycle (deep sleep or reboot)
    unsent_data = load_unsent_data()

    # Get the current time from the RTC using getDS3231.do_getDS3231 function
    dt = get_rtc_data()

    # Get temperature and humidity from DHT22
    temperature, humidity = get_dht22_data()

    # Prepare current reading to be added to the list
    current_reading = {
        "year": dt[0],
        "month": dt[1],
        "day": dt[2],
        "hour": dt[3],
        "minute": dt[4],
        "second": dt[5],
        "temperature": temperature,
        "humidity": humidity
    }

    ssid = "Galaxy A25 5G 6737"
    password = "11111111"

    # Try to connect to Wi-Fi
    wlan = connect_to_wifi(ssid, password)

    # If Wi-Fi is connected, try to send data
    if wlan.isconnected():
        # Send any unsent data from the last session first
        if unsent_data:
            success = True
            for data in unsent_data:
                if not send_data_to_server(data):
                    success = False
                    break
            
            if success:
                delete_unsent_data()  # Clear stored data if all sent successfully

        # Add the current reading to the unsent data list and save it
        unsent_data.append(current_reading)
        save_unsent_data(unsent_data)
    else:
        print("Wi-Fi not connected, storing current reading")
        # Add the current reading to the unsent data list and save it
        unsent_data.append(current_reading)
        save_unsent_data(unsent_data)

    # Disconnect Wi-Fi to save power
    wlan.disconnect()
    wlan.active(False)

    # Enter deep sleep for the specified duration
    print(f"Entering deep sleep for {SLEEP_DURATION / 1000} seconds...")
    # deepsleep(SLEEP_DURATION)

# Start the main loop
main()
