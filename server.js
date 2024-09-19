const express = require('express');
const bodyParser = require('body-parser');
const fs = require('fs');

const app = express();
const port = 3000;

// Middleware to parse incoming JSON requests
app.use(bodyParser.json());

// Route to handle POST requests to /time with JSON data
app.post('/time', (req, res) => {
    const jsonData = req.body;

    // Convert the incoming JSON data to a string and add a newline for separation
    const dataToAppend = JSON.stringify(jsonData, null, 2) + ',\n';

    // Append the data to the file
    fs.appendFile('time.json', dataToAppend, (err) => {
        if (err) {
            console.error('Error appending to file:', err);
            return res.status(500).send('Error appending to file');
        }

        console.log('Data received and appended to file successfully');
        res.send('Data appended successfully!');
    });
});

// Start the server
app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});
