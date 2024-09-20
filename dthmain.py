# dhtmain.py
import network
import ntptime
import time
import machine
from machine import RTC, Pin
from utime import sleep_ms
import utime
import json
import sys
import getDS3231

# Configuration

rtc = RTC()

ssid = "Galaxy A25 5G 6737"

#ssid = "Galaxy A25 5G 6737"
password = "11111111"

ON_BOARD_PIN = 25
led_pin = Pin(ON_BOARD_PIN, Pin.OUT)

INVALID_DATE = 4
NTP_TIMEOUT = 2
NO_NETWORK = 3

MAX_NTP_RETRIES = 5
NTP_RETRY_INTERVAL = 5

# Define reset cause constants
RESET_POWER_ON = machine.PWRON_RESET
RESET_HARDWARE_WATCHDOG = machine.HARD_RESET
RESET_SOFT_RESET = machine.SOFT_RESET
RESET_DEEP_SLEEP = machine.DEEPSLEEP_RESET


def fetch_ntp_time(max_retries):
    ntp_try_count = 0

    while ntp_try_count < max_retries:
        try:
            ntptime.settime()
            current_time = time.mktime(time.localtime())

            if current_time >= 745023322:
                save_current_time(current_time)

                return True

        except Exception as err:
            print(f"Failed to fetch NTP time, retrying ({ntp_try_count + 1}/{max_retries})")
            print(f"Error: {err}")

        ntp_try_count += 1
        utime.sleep_ms(NTP_RETRY_INTERVAL * 1000)

    return False

def connect_wifi():
    import config

    utime.sleep(0.1) #  this could be important, recent posting by robert-hh

    # config.wlan.scan()
    print( config.wlan.status())

    if not config.wlan.isconnected():
        print('connecting to network...')
        config.wlan.connect(ssid, password)
        while not config.wlan.isconnected():
                print(config.wlan.status())
                if config.wlan.status()== 201:
                    break
                utime.sleep(1.0) #  this could be important, recent posting by robert-hh


        utime.sleep(1.0) #  this could be important, recent posting by robert-hh

    if not config.wlan.isconnected():
        print('failed connecting to network...')
        print(config.wlan.status())

    
    if  config.wlan.isconnected():
        print(config.wlan.status())

    if config.wlan.status() == network.STAT_GOT_IP:
        print('Connected to network')


        print('network config:', config.wlan.ifconfig())

    # Get the raw MAC address as a byte string
    mac_byte_string = config.wlan.config('mac')

# Convert the byte string to a human-readable MAC address
    mac_address = ':'.join(['{:02X}'.format(b) for b in mac_byte_string])

# Print the MAC address
    print("MAC address: {}".format(mac_address))

def blink_error(short_blinks):
    while True:
        led_pin.value(1)
        sleep_ms(1000)
        for i in range(short_blinks):
            led_pin.value(0)
            sleep_ms(200)
            led_pin.value(1)
            sleep_ms(200)

        led_pin.value(0)
        sleep_ms(1000)

def save_current_time(current_time):
    try:
        with open("currenttime.json", "w") as file:
            data = {"current_time": current_time}
            json.dump(data, file)
        print("Current time saved to currenttime.json")
    except Exception as err:
        print(f"Error saving current time to JSON file: {err}")

def read_current_time():
    try:
        with open("currenttime.json", "r") as file:
            data = {}
            data = json.load(file)
            return data.get("current_time")
    except Exception as err:
        print(f"Error reading current time from JSON file: {err}")
        return None
    
def print_rtc_time():

    global rtc

    # Get the RTC time components
    rtc_time = rtc.datetime()

    # Format the RTC time as a human-readable string
    rtc_time_str = "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(
        rtc_time[0], rtc_time[1], rtc_time[2], rtc_time[4], rtc_time[5], rtc_time[6]
    )

    # Print the human-readable RTC time
    print("RTC Time:", rtc_time_str)


    
def set_clock():
    global rtc

    if network.WLAN(network.STA_IF).isconnected():
        print("Network is connected, getting NTP")
        if fetch_ntp_time(MAX_NTP_RETRIES):
            print("NTP time successfully obtained.")
        else:
            print("Failed to obtain a valid NTP time after multiple retries.")
            blink_error(NTP_TIMEOUT)
    else:
        print('Wi-Fi was not connected, cannot fetch NTP time')
        saved_time = read_current_time()

        if saved_time is not None:
            print(f"Retrieved Saved time from JSON: {saved_time}")
            # print(time.mktime(time.localtime()))
            print(time.localtime())
            
            rtc.datetime(time.localtime())
            print_rtc_time()

    print(rtc.datetime())
    print_rtc_time()

def main():
    print('Starting dhtmain')

    import machine


# Function to handle reset causes
def handle_power_on_reset():
    print("Power-on reset")

    getDS3231.do_getDS3231()
    

    # connect_wifi()
    # set_clock()
    # print(rtc.datetime())
    # print_rtc_time()
    # import datalog2


def handle_hardware_watchdog_reset():
    print("Hardware watchdog reset")

def handle_soft_reset():
    print("Soft reset")

    print(rtc.datetime())
    print_rtc_time()

    print('Enter REPL')
    sys.exit()

def handle_brown_out_reset():
    print("Brown-out reset")
    
def handle_deep_sleep_reset():
    print("Deep sleep reset")
    # import datalog2
    getDS3231.do_getDS3231


# Get the reset cause
reset_cause = machine.reset_cause()

# Clear the reset cause
machine.wake_reason()


# Create a dictionary to map reset causes to corresponding handler functions
reset_handlers = {
    RESET_POWER_ON: handle_power_on_reset,
    RESET_HARDWARE_WATCHDOG: handle_hardware_watchdog_reset,
    RESET_SOFT_RESET: handle_soft_reset,
    # RESET_BROWN_OUT: handle_brown_out_reset,
    RESET_DEEP_SLEEP: handle_deep_sleep_reset
}

# Call the handler function for the reset cause (if defined)
reset_handlers.get(reset_cause, lambda: print("Unknown reset cause"))()

#currently should never reach here
#sampling delay moved to datalog2 deep sleep time


# Clear the reset cause
machine.wake_reason()

print('sleeping')

sleep_ms(10000)






# if __name__ == "__main__":
#     main()
