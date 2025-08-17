const express = require('express');
const cors = require('cors');
const multer = require('multer');
const path = require('path');
const fs = require('fs');
const { spawn } = require('child_process');

const app = express();
const PORT = process.env.PORT || 3001;

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static('public'));

// Configure multer for file uploads
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    const uploadDir = 'uploads';
    if (!fs.existsSync(uploadDir)) {
      fs.mkdirSync(uploadDir, { recursive: true });
    }
    cb(null, uploadDir);
  },
  filename: (req, file, cb) => {
    const uniqueSuffix = Date.now() + '-' + Math.round(Math.random() * 1E9);
    cb(null, file.fieldname + '-' + uniqueSuffix + path.extname(file.originalname));
  }
});

const upload = multer({ 
  storage: storage,
  fileFilter: (req, file, cb) => {
    const allowedTypes = /jpeg|jpg|png|webp|heic/;
    const extname = allowedTypes.test(path.extname(file.originalname).toLowerCase());
    const mimetype = allowedTypes.test(file.mimetype);
    
    if (extname && mimetype) {
      return cb(null, true);
    } else {
      cb(new Error('Only image files are allowed'));
    }
  },
  limits: {
    fileSize: 50 * 1024 * 1024 // 50MB limit
  }
});

// Helper function to call Python backend functions
const callPythonScript = (scriptName, args = []) => {
  return new Promise((resolve, reject) => {
    const python = spawn('python3', ['backend/' + scriptName, ...args], {
      cwd: path.resolve(__dirname, '..'),
      env: { ...process.env, PYTHONPATH: '.' }
    });
    let data = '';
    let error = '';

    python.stdout.on('data', (chunk) => {
      data += chunk.toString();
    });

    python.stderr.on('data', (chunk) => {
      error += chunk.toString();
    });

    python.on('close', (code) => {
      if (code !== 0) {
        reject(new Error(error || `Python script exited with code ${code}`));
      } else {
        try {
          resolve(JSON.parse(data));
        } catch (e) {
          resolve(data);
        }
      }
    });
  });
};

// API Routes

// Get all projects
app.get('/api/projects', async (req, res) => {
  try {
    const result = await callPythonScript('get_projects.py');
    res.json(result);
  } catch (error) {
    console.error('Error getting projects:', error);
    res.status(500).json({ error: 'Failed to get projects' });
  }
});

// Create new project
app.post('/api/projects', async (req, res) => {
  try {
    const { name, description } = req.body;
    const result = await callPythonScript('create_project.py', [name, description || '']);
    res.json(result);
  } catch (error) {
    console.error('Error creating project:', error);
    res.status(500).json({ error: 'Failed to create project' });
  }
});

// Delete project
app.delete('/api/projects/:id', async (req, res) => {
  try {
    const { id } = req.params;
    const result = await callPythonScript('delete_project.py', [id]);
    res.json(result);
  } catch (error) {
    console.error('Error deleting project:', error);
    res.status(500).json({ error: 'Failed to delete project' });
  }
});

// Get project images
app.get('/api/projects/:id/images', async (req, res) => {
  try {
    const { id } = req.params;
    const result = await callPythonScript('get_project_images.py', [id]);
    res.json(result);
  } catch (error) {
    console.error('Error getting project images:', error);
    res.status(500).json({ error: 'Failed to get project images' });
  }
});

// Upload and process screenshots
app.post('/api/projects/:id/upload', upload.array('screenshots'), async (req, res) => {
  try {
    const { id } = req.params;
    const { processingMode } = req.body;
    const files = req.files;

    if (!files || files.length === 0) {
      return res.status(400).json({ error: 'No files uploaded' });
    }

    // Process files using Python backend
    const filePaths = files.map(file => file.path);
    const result = await callPythonScript('process_screenshots.py', [
      id,
      processingMode || 'Fast Local Vision',
      JSON.stringify(filePaths)
    ]);

    // Clean up uploaded files
    files.forEach(file => {
      try {
        fs.unlinkSync(file.path);
      } catch (err) {
        console.error('Error cleaning up file:', err);
      }
    });

    res.json(result);
  } catch (error) {
    console.error('Error processing screenshots:', error);
    res.status(500).json({ error: 'Failed to process screenshots' });
  }
});

// Search screenshots
app.post('/api/search', async (req, res) => {
  try {
    const { query, projectId, searchMode, maxResults } = req.body;
    
    if (!query || !projectId) {
      return res.status(400).json({ error: 'Query and project ID are required' });
    }

    const result = await callPythonScript('search_screenshots.py', [
      projectId,
      query,
      searchMode || 'combined',
      maxResults || '10'
    ]);

    res.json(result);
  } catch (error) {
    console.error('Error searching screenshots:', error);
    res.status(500).json({ error: 'Failed to search screenshots' });
  }
});

// Health check
app.get('/api/health', (req, res) => {
  res.json({ status: 'OK', timestamp: new Date().toISOString() });
});

// Error handling middleware
app.use((error, req, res, next) => {
  if (error instanceof multer.MulterError) {
    if (error.code === 'LIMIT_FILE_SIZE') {
      return res.status(400).json({ error: 'File too large' });
    }
  }
  
  console.error('Server error:', error);
  res.status(500).json({ error: 'Internal server error' });
});

app.listen(PORT, '0.0.0.0', () => {
  console.log(`Server running on port ${PORT}`);
});