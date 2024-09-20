# print json file

import json

# Define the file path for the JSON file
# data_file = "unsent_data.json"
data_file = "time.json"


# Function to read and print the JSON data from the file
def read_json_file():
    try:
        with open(data_file, "r") as f:
            lines = f.readlines()  # Read all lines from the file
            
            for line in lines:
                data = json.loads(line.strip())  # Parse each line as JSON
                print("Data:", data)  # Print the parsed data
    except Exception as e:
        print("Error reading JSON file:", e)

# Main function to invoke the reading and printing of the file
def main():
    read_json_file()

# Start the program
main()
