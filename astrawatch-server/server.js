const express = require('express');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;
const DATA_DIR = process.env.ASTRAWATCH_DATA_DIR || path.join(__dirname, 'data');
const SUBMISSIONS_FILE = path.join(DATA_DIR, 'waitlist.json');

// Ensure data directory exists
if (!fs.existsSync(DATA_DIR)) {
  fs.mkdirSync(DATA_DIR, { recursive: true });
}

// Middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname, 'public')));

// CORS for direct API access
app.use((req, res, next) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.sendStatus(200);
  next();
});

// Health check
app.get('/health', (req, res) => {
  res.json({ status: 'ok', service: 'astrawatch-waitlist', uptime: process.uptime() });
});

// Waitlist signup count
app.get('/api/waitlist', (req, res) => {
  try {
    const data = fs.existsSync(SUBMISSIONS_FILE)
      ? JSON.parse(fs.readFileSync(SUBMISSIONS_FILE, 'utf-8'))
      : [];
    res.json({ count: data.length, signups: data.map(s => ({ name: s.name, company: s.company, practiceArea: s.practiceArea, firmSize: s.firmSize, createdAt: s.createdAt })) });
  } catch (err) {
    res.status(500).json({ error: 'Failed to read submissions' });
  }
});

// Waitlist signup
app.post('/api/waitlist', (req, res) => {
  const { name, email, company, practiceArea, firmSize } = req.body;

  // Validate required fields
  if (!name || !email || !company || !practiceArea) {
    return res.status(400).json({ error: 'Missing required fields: name, email, company, practiceArea' });
  }

  // Basic email validation
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(email)) {
    return res.status(400).json({ error: 'Invalid email format' });
  }

  const signup = {
    id: Date.now().toString(36) + Math.random().toString(36).slice(2, 6),
    name,
    email,
    company,
    practiceArea: practiceArea || 'other',
    firmSize: firmSize || null,
    createdAt: new Date().toISOString(),
    source: req.headers['user-agent'] || 'unknown'
  };

  try {
    const data = fs.existsSync(SUBMISSIONS_FILE)
      ? JSON.parse(fs.readFileSync(SUBMISSIONS_FILE, 'utf-8'))
      : [];
    data.push(signup);
    fs.writeFileSync(SUBMISSIONS_FILE, JSON.stringify(data, null, 2));

    console.log(`[WAITLIST] ${signup.name} <${signup.email}> — ${signup.company} (${signup.practiceArea})`);
    res.status(201).json({ success: true, message: 'You\'re on the list!' });
  } catch (err) {
    console.error('[WAITLIST] Failed to save:', err.message);
    res.status(500).json({ error: 'Failed to save signup. Please try again.' });
  }
});

// Catch-all: serve index.html for SPA-like routing
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.listen(PORT, () => {
  console.log(`AstraWatch landing server running on port ${PORT}`);
  console.log(`Data directory: ${DATA_DIR}`);
});
