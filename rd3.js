// rd3.js
const fs = require('fs');
const readline = require('readline');

// Read the file named 'unsent_data.json'
fs.readFile('unsent_data.json', 'utf8', (err, data) => {
    if (err) {
        console.error('Error reading unsent_data.json:', err);
        return;
    }

    // Output the data to 'time.json'
    fs.writeFile('time.json', data, (err) => {
        if (err) {
            console.error('Error writing to time.json:', err);
            return;
        }

        // Create a readline interface to read 'time.json' line by line
        const rl = readline.createInterface({
            input: fs.createReadStream('time.json'),
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
            // Now that all lines have been read and parsed, print the array
            console.log('Array of dth:', dthArray);
        });
    });
});
