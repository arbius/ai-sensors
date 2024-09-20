// rd2.js
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

        let lines = [];

        // Read each line of 'time.json' and store it in an array
        rl.on('line', (line) => {
            lines.push(line); // Store each line in the array
        });

        rl.on('close', () => {
            // Now the file has been read into the 'lines' array, print it
            console.log('Contents of time.json, line by line:', lines);
            // Access the lines via the array
            console.log('First line:', lines[0]); // Example of accessing a line
        });
    });
});
