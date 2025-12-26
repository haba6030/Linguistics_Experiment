/**
 * Simple Node.js + Express server for saving jsPsych data
 *
 * SETUP INSTRUCTIONS:
 * 1. Install Node.js from https://nodejs.org/
 * 2. Open terminal in this directory
 * 3. Run: npm init -y
 * 4. Run: npm install express cors
 * 5. Run: node server.js
 * 6. Server will run on http://localhost:3000
 */

const express = require('express');
const cors = require('cors');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = 3000;

// Middleware
app.use(cors()); // Allow cross-origin requests
app.use(express.json({ limit: '50mb' })); // Parse JSON bodies (increased limit for large datasets)
app.use(express.static('.')); // Serve static files from current directory

// Create data directory if it doesn't exist
const DATA_DIR = path.join(__dirname, 'data');
if (!fs.existsSync(DATA_DIR)) {
  fs.mkdirSync(DATA_DIR);
  console.log('Created data directory:', DATA_DIR);
}

// ============================================================================
// ROUTES
// ============================================================================

/**
 * Health check endpoint
 */
app.get('/', (req, res) => {
  res.send(`
    <html>
      <head>
        <title>Talren SPR Server</title>
        <style>
          body { font-family: Arial, sans-serif; padding: 40px; max-width: 800px; margin: 0 auto; }
          h1 { color: #4CAF50; }
          code { background-color: #f4f4f4; padding: 2px 6px; border-radius: 3px; }
        </style>
      </head>
      <body>
        <h1>Talren SPR Experiment Server</h1>
        <p>Server is running successfully!</p>
        <h2>Status</h2>
        <ul>
          <li>Port: ${PORT}</li>
          <li>Data directory: ${DATA_DIR}</li>
          <li>Time: ${new Date().toLocaleString()}</li>
        </ul>
        <h2>Available Endpoints</h2>
        <ul>
          <li><code>POST /save-data</code> - Save experiment data</li>
          <li><code>GET /data-files</code> - List all saved data files</li>
        </ul>
        <h2>Usage</h2>
        <p>To run the experiment, open <code>index.html</code> in a web browser.</p>
        <p>Make sure to uncomment the <code>saveDataToServer()</code> call in <code>experiment.js</code> if you want to use server-side data saving.</p>
      </body>
    </html>
  `);
});

/**
 * Save experiment data endpoint
 * Receives POST request with experiment data and saves it to a JSON file
 */
app.post('/save-data', (req, res) => {
  try {
    const { participant_id, list_id, data } = req.body;

    if (!participant_id || !list_id || !data) {
      return res.status(400).json({
        success: false,
        error: 'Missing required fields: participant_id, list_id, or data'
      });
    }

    // Create filename with timestamp
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const filename = `talren_spr_p${participant_id}_list${list_id}_${timestamp}.json`;
    const filepath = path.join(DATA_DIR, filename);

    // Prepare data object
    const dataToSave = {
      participant_id: participant_id,
      list_id: list_id,
      timestamp: new Date().toISOString(),
      data: data
    };

    // Save to file
    fs.writeFileSync(filepath, JSON.stringify(dataToSave, null, 2), 'utf8');

    console.log(`Data saved: ${filename}`);

    res.json({
      success: true,
      message: 'Data saved successfully',
      filename: filename,
      participant_id: participant_id,
      list_id: list_id
    });

  } catch (error) {
    console.error('Error saving data:', error);
    res.status(500).json({
      success: false,
      error: 'Server error while saving data',
      details: error.message
    });
  }
});

/**
 * List all saved data files
 */
app.get('/data-files', (req, res) => {
  try {
    const files = fs.readdirSync(DATA_DIR)
      .filter(file => file.endsWith('.json'))
      .map(file => ({
        filename: file,
        path: path.join(DATA_DIR, file),
        size: fs.statSync(path.join(DATA_DIR, file)).size,
        created: fs.statSync(path.join(DATA_DIR, file)).birthtime
      }))
      .sort((a, b) => b.created - a.created); // Sort by most recent first

    res.json({
      success: true,
      count: files.length,
      files: files
    });

  } catch (error) {
    console.error('Error listing data files:', error);
    res.status(500).json({
      success: false,
      error: 'Server error while listing files',
      details: error.message
    });
  }
});

/**
 * Optional: Download a specific data file
 */
app.get('/download/:filename', (req, res) => {
  try {
    const filename = req.params.filename;
    const filepath = path.join(DATA_DIR, filename);

    if (!fs.existsSync(filepath)) {
      return res.status(404).json({
        success: false,
        error: 'File not found'
      });
    }

    res.download(filepath);

  } catch (error) {
    console.error('Error downloading file:', error);
    res.status(500).json({
      success: false,
      error: 'Server error while downloading file',
      details: error.message
    });
  }
});

// ============================================================================
// START SERVER
// ============================================================================

app.listen(PORT, () => {
  console.log('='.repeat(60));
  console.log('Talren SPR Experiment Server');
  console.log('='.repeat(60));
  console.log(`Server is running on http://localhost:${PORT}`);
  console.log(`Data will be saved to: ${DATA_DIR}`);
  console.log('Press Ctrl+C to stop the server');
  console.log('='.repeat(60));
});

// Handle graceful shutdown
process.on('SIGINT', () => {
  console.log('\n\nShutting down server...');
  process.exit(0);
});
