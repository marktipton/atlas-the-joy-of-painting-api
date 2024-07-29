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

// Endpoint to filter episodes
app.get('/episodes', async (req, res) => {
  const { month, subjects, colors, match_all } = req.query;

  let query = `SELECT e.id, e.painting_index, e.img_src, e.title, e.season, e.episode_number, e.youtube_src, e.date, e.month, e.day, e.year, e.note
               FROM episodes e
               LEFT JOIN episodes_subjects es ON e.id = es.episode_id
               LEFT JOIN subjects s ON es.subject_id = s.id
               LEFT JOIN episodes_colors ec ON e.id = ec.episode_id
               LEFT JOIN colors c ON ec.color_id = c.id
               WHERE 1=1`;

  // Filters
  const params = [];
  let paramIndex = 1;

  if (month) {
    query += ` AND e.month = $${paramIndex++}`;
    params.push(month);
  }

  if (subjects) {
    const subjectsArray = subjects.split(',');
    query += ` AND s.subject_name = ANY($${paramIndex++}::text[])`;
    params.push(subjectsArray);
  }

  if (colors) {
    const colorsArray = colors.split(',');
    query += ` AND c.color_name = ANY($${paramIndex++}::text[])`;
    params.push(colorsArray);
  }

  // Match all or any
  if (match_all === 'true') {
    query += ` GROUP BY e.id HAVING COUNT(DISTINCT s.subject_name) = $${paramIndex++} AND COUNT(DISTINCT c.color_name) = $${paramIndex++}`;
    params.push(subjects ? subjects.split(',').length : 0);
    params.push(colors ? colors.split(',').length : 0);
  }

  try {
    const result = await pool.query(query, params);
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