// rd.js
const fs = require('fs');

// Read the file named 'unused_data.json'
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

        // Read the 'time.json' file back into a variable named rd
        fs.readFile('time.json', 'utf8', (err, rd) => {
            if (err) {
                console.error('Error reading time.json:', err);
                return;
            }

            // Print rd
            console.log('Contents of rd:', rd);
        });
    });
});
