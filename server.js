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

app.get('/episodes', async (req, res) => {
  try {
    const result = await pool.query('SELECT * FROM episodes');
    res.json(result.rows);
  } catch (error) {
    console.error(error);
    res.status(500).send('Server error');
  }
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
app.get('/episodes/subjects', async (req, res) => {
  const { subjects } = req.query;

  if (subjects) {
    const subjectsArray = subjects.split(',');
    console.log(subjectsArray);
    try {
      const result = await pool.query(
        `SELECT e.id, e.painting_index, e.img_src, e.title, e.season, e.episode_number, e.youtube_src, e.date, e.month, e.day, e.year, e.note
         FROM episodes e
         JOIN episodes_subjects es ON e.id = es.episode_id
         JOIN subjects s ON es.subject_id = s.id
         WHERE s.subject_name = ANY($1::text[])
         GROUP BY e.id, e.painting_index, e.img_src, e.title, e.season, e.episode_number, e.youtube_src, e.date, e.month, e.day, e.year, e.note
         HAVING COUNT(DISTINCT s.subject_name) = $2`,
        [subjectsArray, subjectsArray.length]
      );
      res.json(result.rows);
    } catch (error) {
      console.error(error);
      res.status(500).send('Server error');
    }
  } else {
    // If no query parameter is provided, return the list of subjects
    try {
      const result = await pool.query('SELECT * FROM subjects');
      res.json({
        message: 'All subjects are listed below. Choose one or more to find information about the episodes with those subjects present',
        data: result.rows
      });
    } catch (error) {
      console.error(error);
      res.status(500).send('Server error');
    }
  }
});

app.get('/episodes/colors', async (req, res) => {
  const { colors } = req.query;

  if (colors) {
    const colorsArray = colors.split(',');
    try {
      // SQL query to find episodes that contain all the specified colors
      const result = await pool.query(
        `SELECT e.id, e.painting_index, e.img_src, e.title, e.season, e.episode_number, e.youtube_src, e.date, e.month, e.day, e.year, e.note
         FROM episodes e
         JOIN episodes_colors ec ON e.id = ec.episode_id
         JOIN colors c ON ec.color_id = c.id
         WHERE c.color_name = ANY($1::text[])
         GROUP BY e.id
         HAVING COUNT(DISTINCT c.color_name) = $2`,
        [colorsArray, colorsArray.length]
      );
      res.json(result.rows);
    } catch (error) {
      console.error(error);
      res.status(500).send('Server error');
    }
  } else {
    // If no query parameter is provided, return the list of colors
    try {
      const result = await pool.query('SELECT * FROM colors');
      res.json({
        message: 'All colors are listed below. Choose one or more to find information about the episodes with those colors present',
        data: result.rows
      });
    } catch (error) {
      console.error(error);
      res.status(500).send('Server error');
    }
  }
});

// app.get('/episodes/filter', async (req, res) => {
//   const { month, subjects, colors, match_all } = req.query;

//   let query = `
//     SELECT DISTINCT e.id, e.painting_index, e.img_src, e.title, e.season, e.episode_number, e.youtube_src, e.date, e.month, e.day, e.year, e.note
//     FROM episodes e
//     LEFT JOIN episodes_subjects es ON e.id = es.episode_id
//     LEFT JOIN subjects s ON es.subject_id = s.id
//     LEFT JOIN episodes_colors ec ON e.id = ec.episode_id
//     LEFT JOIN colors c ON ec.color_id = c.id
//     WHERE 1=1
//   `;

//   const params = [];
//   let paramIndex = 1;

//   if (month) {
//     query += ` AND e.month = $${paramIndex++}`;
//     params.push(month);
//   }

//   if (subjects) {
//     const subjectsArray = subjects.split(',');
//     query += ` AND s.subject_name = ANY($${paramIndex++}::text[])`;
//     params.push(subjectsArray);
//   }

//   if (colors) {
//     const colorsArray = colors.split(',');
//     query += ` AND c.color_name = ANY($${paramIndex++}::text[])`;
//     params.push(colorsArray);
//   }

//   // Match all or any
//   if (match_all === 'true') {
//     if (subjects) {
//       query += ` GROUP BY e.id HAVING COUNT(DISTINCT s.subject_name) = $${paramIndex++}`;
//       params.push(subjects.split(',').length);
//     }
//     if (colors) {
//       query += ` AND COUNT(DISTINCT c.color_name) = $${paramIndex++}`;
//       params.push(colors.split(',').length);
//     }
//   } else {
//     query += ` GROUP BY e.id`;
//   }

//   try {
//     const result = await pool.query(query, params);
//     res.json(result.rows);
//   } catch (error) {
//     console.error(error);
//     res.status(500).send('Server error');
//   }
// });
// Start server
app.listen(port, () => {
  console.log(`Server running on http://localhost:${port}`);
});