import network
import time
from machine import Pin, deepsleep, RTC
import dht
import urequests
import ujson
import getDS3231

SLEEP_DURATION = 10 * 1000  # Sleep for 60 seconds
rtc = RTC()
server_url = "http://Insp16.local:3000/time"
data_file = "unsent_data.json"  # File to store unsent data when Wi-Fi or server is unavailable

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

# Initialize DHT22 sensor (DHT22 connected to pin 15)
dht22_sensor = dht.DHT22(Pin(15))

# Get time from DS3231 RTC using getDS3231.do_getDS3231 function
def get_rtc_data():
    try:
        dt = getDS3231.do_getDS3231()
        if len(dt) >= 7:  # Ensure the data has the expected number of elements
            year = dt[0]    # Year
            month = dt[1]   # Month
            day = dt[2]     # Day
            hour = dt[3]    # Hour (index 3)
            minute = dt[4]  # Minute
            second = dt[5]  # Second

            print(f"RTC Data: Year: {year}, Month: {month}, Day: {day}, Hour: {hour}, Minute: {minute}, Second: {second}")
            return year, month, day, hour, minute, second
        else:
            print("Unexpected RTC data format:", dt)
            return (0, 0, 0, 0, 0, 0)  # Return default values in case of error
    except Exception as e:
        print("Failed to get RTC data:", e)
        return (0, 0, 0, 0, 0, 0)  # Return default values in case of error

# Get temperature and humidity from DHT22
def get_dht22_data():
    try:
        dht22_sensor.measure()
        temperature = dht22_sensor.temperature()
        humidity = dht22_sensor.humidity()
        return temperature, humidity
    except Exception as e:
        print("Failed to read from DHT22:", e)
        return None, None

# Send data to the Node.js server
def send_data_to_server(data):
    try:
        response = urequests.post(server_url, json=data)
        print("Server response:", response.text)
        response.close()
        return True  # Successfully sent
    except Exception as e:
        print("Failed to send data:", e)
        return False  # Failed to send

# Append unsent data to the local file
def append_unsent_data(data):
    try:
        with open(data_file, "a") as f:
            data = ujson.dumps(data)
            f.write(data + "\n")  # Append each entry on a new line
        print("Data appended to local storage.")
    except Exception as e:
        print("Failed to append data:", e)

# Send stored data from the file to the server
def send_stored_data():
    try:
        with open(data_file, "r") as f:
            lines = f.readlines()
        
        for line in lines:
            data = ujson.loads(line.strip())
            if send_data_to_server(data):
                print("Stored data sent successfully!")
            else:
                print("Failed to send stored data.")
                return  # Stop if there's a failure

        # Clear the file if all data was sent successfully
        with open(data_file, "w") as f:
            f.write("")  # Overwrite the file with an empty string
    except Exception as e:
        print("Failed to read or send stored data:", e)

# Main function to collect and send data
def main():
    # Get the current time from the RTC
    year, month, day, hour, minute, second = get_rtc_data()

    # Get temperature and humidity from DHT22
    temperature, humidity = get_dht22_data()

    # Prepare data in JSON format
    data = {
        "year": year,
        "month": month,
        "day": day,
        "hour": hour,
        "minute": minute,
        "second": second,
        "temperature": temperature,
        "humidity": humidity
    }

    print("Data to be sent:", ujson.dumps(data))

    # Connect to Wi-Fi
    ssid = "Galaxy A25 5G 6737"
    password = "11111111"
    wlan = connect_to_wifi(ssid, password)

    # If Wi-Fi is connected, attempt to send both current and stored data
    if wlan.isconnected():
        send_stored_data()  # Try to send any unsent data from previous attempts

        # Try sending the current data
        if send_data_to_server(data):
            print("Data sent successfully!")
        else:
            print("Failed to send current data. Appending to local storage.")
            append_unsent_data(data)
    else:
        print("Wi-Fi not connected, appending data to local storage.")
        append_unsent_data(data)

    # Disconnect Wi-Fi and go to sleep
    wlan.disconnect()
    wlan.active(False)

    # Enter deep sleep for the specified duration
    print(f"Entering deep sleep for {SLEEP_DURATION / 1000} seconds...")
    deepsleep(SLEEP_DURATION)

# Start the main loop
main()
