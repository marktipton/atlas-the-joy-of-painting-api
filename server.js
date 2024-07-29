const express = require('express');
const { Pool } = require('pg');
const bodyParser = require('body-parser');

const app = express();
const port = 3000; // or any port you prefer

app.use(bodyParser.json()); // for parsing application/json

// PostgreSQL connection configuration
const pool = new Pool({
  user: 'bob',
  host: 'localhost',
  database: 'joyofcoding',
  password: 'ross',
  port: 5432,
});

app.get('/episodes/month', async (req, res) => {
  const { month } = req.query;
  if (!month) {
    return res.status(400).send('Month parameter is required');
  }

  try {
    const result = await pool.query(
      `SELECT * FROM episodes WHERE month = $1`,
      [month]
    );
    res.json(result.rows);
  } catch (error) {
    console.error(error);
    res.status(500).send('Server error');
  }
});

// Start server
app.listen(port, () => {
  console.log(`Server running on http://localhost:${port}`);
});