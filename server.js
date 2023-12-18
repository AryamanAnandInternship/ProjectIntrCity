const express = require('express');
const mysql = require('mysql2');
const bodyParser = require('body-parser');

const app = express();
const port = 3000; // or any port you prefer

// Create a MySQL pool
const pool = mysql.createPool({
  host: '172.16.123.198',
  user: 'readonly',
  password: 're@diQ0_yL8^sM0?kV6)',
  database: 'gds_operations',
  waitForConnections: true,
  connectionLimit: 10,
  queueLimit: 0
});

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// API endpoint to handle bus route data retrieval
app.get('/bus/:busId', (req, res) => {
  const busId = req.params.busId;

  // Query the database for bus route data
  pool.query('select * from bus_service_run_eta_details where bus_service_run_etum_id=192013 order by si_no asc',[busId],  (err, results) => {
    if (err) {
      console.error('Error querying database:', err);
      res.status(500).send('Internal Server Error');
    } else {
      res.json(results);
    }
  });
});

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
