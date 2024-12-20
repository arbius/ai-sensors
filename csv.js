// csv.js

const fs = require('fs');
const readline = require('readline');

// Read the file named 'time.json'
fs.readFile('time.json', 'utf8', (err, data) => {
    if (err) {
        console.error('Error reading time.json:', err);
        return;
    }

    // Output the data to 'dth.json'
    fs.writeFile('dth.json', data, (err) => {
        if (err) {
            console.error('Error writing to dth.json:', err);
            return;
        }

        // Create a readline interface to read 'time.json' line by line
        const rl = readline.createInterface({
            input: fs.createReadStream('dth.json'),
            output: process.stdout,
            terminal: false
        });

        let dthArray = [];

        // Read each line of 'time.json' and parse it into a JS object
        rl.on('line', (line) => {
            try {
                const dth = JSON.parse(line); // Parse each line into a JS object
                dthArray.push(dth); // Store the dth object in the array
            } catch (err) {
                console.error('Error parsing line as JSON:', err);
            }
        });

        rl.on('close', () => {
            if (dthArray.length > 0) {
                // Define the desired key order
                const keyOrder = ['day', 'month', 'year', 'hour', 'minute', 'second', 'temperature', 'humidity', 'iso_timestamp']; // Specify the order you want (e.g., age first, then name)

                // Create the CSV file 'dth.csv'
                const csvFile = fs.createWriteStream('dth.csv');

                // Write the header with the specified key order
                csvFile.write(keyOrder.join(',') + '\n');

                // Iterate over the array and write the values in the desired order
                dthArray.forEach((dth) => {
                    const values = keyOrder.map(key => dth[key] || ''); // Get values in the desired order
                    csvFile.write(values.join(',') + '\n');
                });

                console.log('CSV file "dth.csv" created successfully with reordered keys.');

                // Ask the user if they want to delete the input file
                askToDeleteInputFile();
                
            } else {
                console.log('No data to write to the CSV file.');
            }
        });
    });
});

// Function to ask the user if they want to delete the input file
function askToDeleteInputFile() {
    const rl = readline.createInterface({
        input: process.stdin,
        output: process.stdout
    });

    rl.question('Do you want to delete the input file (time.json)? (yes/no): ', (answer) => {
        if (answer.toLowerCase() === 'yes' || answer.toLowerCase() === 'y') {
            deleteInputFile('time.json');
        } else {
            console.log('Input file not deleted.');
        }
        rl.close();
    });
}

// Function to delete the input file
function deleteInputFile(filePath) {
    fs.unlink(filePath, (err) => {
        if (err) {
            console.error(`Error deleting ${filePath}:`, err);
        } else {
            console.log(`Successfully deleted ${filePath}.`);
        }
    });
}










