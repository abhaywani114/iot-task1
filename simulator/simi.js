const net = require('net');
const mysql = require('mysql');
const moment = require('moment');

const PORT = 8888;
const verbose = process.argv.includes('--verbose');

// Create a MySQL database connection
const connection = mysql.createConnection({
    host: 'localhost',
    user: 'root',
    password: 'root',
    database: 'mytest'
});

// Connect to the database
connection.connect(err => {
    if (err) {
        console.error('Error connecting to MySQL database:', err);
        return;
    }
    console.log('Connected to MySQL database');
});

// Create a TCP server
const server = net.createServer(socket => {
    console.log('Client connected.');

    socket.on('data', data => {
        const receivedData = JSON.parse(data.toString());
        console.log(`Received data from ${receivedData.device_id}:`, receivedData);

        // Convert Unix timestamp with milliseconds to a MySQL datetime format
        const timestamp = moment(receivedData.timestamp * 1000).format('YYYY-MM-DD HH:mm:ss');

        if (verbose) {
            console.log('Inserting data into MySQL database...');
        }

        // Insert the received data into the MySQL database
        const query = 'INSERT INTO iot_data (device_id, timestamp, data) VALUES (?, ?, ?)';
        const values = [receivedData.device_id, timestamp, receivedData.data];
        connection.query(query, values, (err, result) => {
            if (err) {
                console.error('Error inserting data into MySQL database:', err);
                return;
            }
            if (verbose) {
                console.log('Data inserted into MySQL database:', result);
            }
        });
    });

    socket.on('end', () => {
        console.log('Client disconnected.');
    });

    socket.on('error', err => {
        console.error('Socket error:', err);
    });
});

server.listen(PORT, () => {
    console.log(`Server is listening on port ${PORT}`);
});

