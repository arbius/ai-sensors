// rs.js
const fs = require('fs');

// Read the stringified JSON file
fs.readFile('time.json', 'utf8', (err, data) => {
  if (err) {
    console.error('Error reading the file:', err);
    return;
  }
  
  // Parse the JSON string into an object
  try {
    console.log(data)
    const jsonData = JSON.parse(data);
    console.log(jsonData);
  } catch (parseErr) {
    console.error('Error parsing JSON:', parseErr);
  }
});
