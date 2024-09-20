#import dht
import json
import uos

def read_data_from_file():
    # filename = "data.json"
    filename = "unsent_data.json"  # File to store unsent data when Wi-Fi or server is unavailable


    data_dict = {}

    if filename in uos.listdir():
        print(f"The file '{filename}' exists.")
        try:
            with open(filename, "r") as file:
                lines = file.readlines()
                for line in lines:
                    if line.strip():  # Skip empty lines
                        data = json.loads(line)
                        data_dict[data["value1"]] = {
                            "temperature": data["value2"],
                            "humidity": data["value3"]
                        }
        except Exception as e:
            print("Error reading data from file:", e)

        return data_dict

def print_dht():
    for count, (key, value) in enumerate(data_dict.items(), start=1):
        print(f"Count: {count}")
        print(f"Key: {key}")
        print(f"Temperature: {value['temperature']}")
        print(f"Humidity: {value['humidity']}")
        print()    


# Usage
data_dict = read_data_from_file()
if data_dict:
    print_dht()
else:
    print('No data read from file')
    

