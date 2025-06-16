const fs = require('fs');
const express = require('express');
const bodyParser = require('body-parser');
const bcrypt = require('bcryptjs');
const { Client } = require('pg');
require('dotenv').config();
const jwt = require('jsonwebtoken');

const app = express();
const port = 3000;

app.use(bodyParser.json());


JWT_SECRET = process.env.JWT_SECRET;

const client = new Client({
  user: process.env.DATABASE_USER,
  host: process.env.DATABASE_HOST,
  database: process.env.DATABASE_NAME,
  password: process.env.DATABASE_PASSWORD,
  port: process.env.DATABASE_PORT,
});


client.connect()
  .then(() => console.log('Connected to PostgreSQL'))
  .catch(err => console.error('Connection error', err.stack));

// Allowed user types
const allowedUserTypes = ['customer', 'eventmanager'];

// Signup Endpoint
app.post('/api/users/signup', async (req, res) => {
  const { username, password, usertype } = req.body;
  
  if (!username || !password || !usertype) {
    return res.status(400).send('Username, password, and userType are required.');
  }

  // Validate userType
  if (!allowedUserTypes.includes(usertype.toLowerCase())) {
    return res.status(400).send('Invalid userType. Allowed values: customer, eventmanager.');
  }

  try {
    // Check if the user already exists
    const existingUser = await client.query(
      'SELECT * FROM users WHERE username = $1', [username]
    );

    if (existingUser.rows.length > 0) {
      return res.status(400).send('Username already taken.');
    }

    // Hash password and create new user
    const hashedPassword = await bcrypt.hash(password, 10);
    const result = await client.query(
      'INSERT INTO users (username, password, usertype) VALUES ($1, $2, $3) RETURNING *',
      [username, hashedPassword, usertype.toLowerCase()]
    );

    res.status(201).send(`User ${result.rows[0].username} created successfully as ${result.rows[0].usertype}.`);
    
  } catch (err) {
    console.error(err);
    res.status(500).send('Server error.');
  }
});

// Login Endpoint
app.post('/api/users/login', async (req, res) => {
  const { username, password } = req.body;
  
  if (!username || !password) {
    return res.status(400).send('Username and password are required.');
  }

  try {
    const result = await client.query('SELECT * FROM users WHERE username = $1', [username]);

    if (result.rows.length === 0) {
      return res.status(400).send('Invalid credentials.');
    }

    const user = result.rows[0];
    const isMatch = await bcrypt.compare(password, user.password);

    if (!isMatch) {
      return res.status(400).send('Invalid credentials.');
    }

    const token = jwt.sign(
      { id: user.userid, username: user.username, usertype: user.usertype },
      JWT_SECRET,
      { expiresIn: '1h' }
    );

    res.status(200).json({ message: `Welcome, ${user.username}!`, token, user_id: user.userid });
  } catch (err) {
    console.error(err);
    res.status(500).send('Server error.');
  }
});

app.listen(port, () => {
  console.log(`Server running on http://localhost:${port}`);
});
