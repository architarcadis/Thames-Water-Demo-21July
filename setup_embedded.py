#!/usr/bin/env python3
"""
Setup script for embedding Smart Acquisition with another app
"""

import os
import json

def create_replit_config():
    """Create .replit configuration for multi-service setup"""
    config = """
# Multi-service configuration
modules = ["python-3.11", "nodejs-20"]

[nix]
channel = "stable-24_05"

[[ports]]
localPort = 5000
externalPort = 80

[[ports]]
localPort = 8000
externalPort = 8000

[[ports]]
localPort = 3000
externalPort = 3000

[deployment]
run = ["python", "main_app.py"]
deploymentTarget = "cloudrun"

[languages]

[languages.python3]
pattern = "**/*.py"

[languages.python3.languageServer]
start = "pylsp"

[languages.javascript]
pattern = "**/{*.js,*.jsx,*.ts,*.tsx,*.mjs,*.cjs}"

[languages.javascript.languageServer]
start = "typescript-language-server --stdio"
"""
    with open('.replit', 'w') as f:
        f.write(config)

def create_package_json():
    """Create package.json for Node.js dependencies if needed"""
    package_json = {
        "name": "smart-acquisition-embedded",
        "version": "1.0.0", 
        "description": "Smart Acquisition with embedded capabilities",
        "scripts": {
            "start": "node server.js",
            "dev": "node server.js"
        },
        "dependencies": {
            "express": "^4.18.2",
            "cors": "^2.8.5",
            "http-proxy-middleware": "^2.0.6"
        }
    }
    
    with open('package.json', 'w') as f:
        json.dump(package_json, f, indent=2)

def create_node_proxy_server():
    """Create a Node.js proxy server for more advanced embedding"""
    server_js = """
const express = require('express');
const { createProxyMiddleware } = require('http-proxy-middleware');
const cors = require('cors');
const path = require('path');

const app = express();
const PORT = 3000;

// Enable CORS for all routes
app.use(cors());

// Serve static files
app.use('/static', express.static('static'));

// Main dashboard route
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'embedded_dashboard.html'));
});

// Proxy Streamlit app
app.use('/streamlit', createProxyMiddleware({
  target: 'http://localhost:5000',
  changeOrigin: true,
  pathRewrite: {
    '^/streamlit': '',
  },
  onProxyReq: (proxyReq, req, res) => {
    // Handle WebSocket connections for Streamlit
    if (req.headers.upgrade === 'websocket') {
      proxyReq.setHeader('Connection', 'upgrade');
      proxyReq.setHeader('Upgrade', 'websocket');
    }
  }
}));

// API routes for your other app
app.get('/api/health', (req, res) => {
  res.json({ status: 'healthy', services: ['streamlit', 'api'] });
});

app.listen(PORT, () => {
  console.log(`Embedded dashboard server running on port ${PORT}`);
  console.log(`Access your integrated app at: http://localhost:${PORT}`);
});
"""
    
    with open('server.js', 'w') as f:
        f.write(server_js)

def create_embedded_html():
    """Create embedded dashboard HTML"""
    html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Smart Acquisition - Integrated Platform</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #1a1a1a;
            color: white;
        }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 1rem 2rem;
            box-shadow: 0 2px 10px rgba(0,0,0,0.3);
        }
        
        .header h1 {
            font-size: 2rem;
            font-weight: 300;
        }
        
        .nav {
            background-color: #2d2d2d;
            padding: 1rem 2rem;
            display: flex;
            gap: 1rem;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
        }
        
        .nav-btn {
            background: linear-gradient(45deg, #4a90e2, #357abd);
            color: white;
            border: none;
            padding: 0.75rem 1.5rem;
            border-radius: 25px;
            cursor: pointer;
            font-weight: 500;
            transition: all 0.3s ease;
        }
        
        .nav-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(74, 144, 226, 0.4);
        }
        
        .nav-btn.active {
            background: linear-gradient(45deg, #ff6b6b, #ee5a5a);
        }
        
        .content-container {
            height: calc(100vh - 140px);
            position: relative;
        }
        
        .content-frame {
            width: 100%;
            height: 100%;
            border: none;
            background: white;
        }
        
        .loading {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            color: #ccc;
            font-size: 1.2rem;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🎯 Smart Acquisition - Integrated Intelligence Platform</h1>
    </div>
    
    <nav class="nav">
        <button class="nav-btn active" onclick="loadContent('streamlit')">
            📊 Market Intelligence
        </button>
        <button class="nav-btn" onclick="loadContent('api')">
            🔧 API Console
        </button>
        <button class="nav-btn" onclick="loadContent('settings')">
            ⚙️ Settings
        </button>
    </nav>
    
    <div class="content-container">
        <div class="loading" id="loading">Loading...</div>
        <iframe class="content-frame" id="contentFrame" src="/streamlit" onload="hideLoading()"></iframe>
    </div>
    
    <script>
        function loadContent(type) {
            const frame = document.getElementById('contentFrame');
            const loading = document.getElementById('loading');
            const buttons = document.querySelectorAll('.nav-btn');
            
            // Update active button
            buttons.forEach(btn => btn.classList.remove('active'));
            event.target.classList.add('active');
            
            // Show loading
            loading.style.display = 'block';
            
            // Load content
            switch(type) {
                case 'streamlit':
                    frame.src = '/streamlit';
                    break;
                case 'api':
                    frame.src = 'data:text/html;charset=utf-8,' + encodeURIComponent(`
                        <div style="padding: 2rem; font-family: Arial, sans-serif;">
                            <h2>API Console</h2>
                            <p>This is where you can integrate other applications or API documentation.</p>
                            <pre style="background: #f4f4f4; padding: 1rem; border-radius: 4px;">
GET /api/health - Check service status
GET /api/market-data - Get market intelligence data
POST /api/search - Execute market search
                            </pre>
                        </div>
                    `);
                    break;
                case 'settings':
                    frame.src = 'data:text/html;charset=utf-8,' + encodeURIComponent(`
                        <div style="padding: 2rem; font-family: Arial, sans-serif;">
                            <h2>Settings</h2>
                            <p>Configuration options for the integrated platform.</p>
                            <form>
                                <label>API Keys:</label><br>
                                <input type="password" placeholder="OpenAI API Key" style="width: 300px; margin: 0.5rem 0; padding: 0.5rem;"><br>
                                <input type="password" placeholder="Google API Key" style="width: 300px; margin: 0.5rem 0; padding: 0.5rem;"><br>
                                <button type="button" style="padding: 0.5rem 1rem; margin-top: 1rem;">Save Settings</button>
                            </form>
                        </div>
                    `);
                    break;
            }
        }
        
        function hideLoading() {
            document.getElementById('loading').style.display = 'none';
        }
    </script>
</body>
</html>
"""
    
    with open('embedded_dashboard.html', 'w') as f:
        f.write(html)

def create_run_script():
    """Create a run script for the embedded setup"""
    script = """#!/bin/bash
echo "Starting Smart Acquisition - Embedded Setup"
echo "=========================================="

# Start Streamlit in background
echo "Starting Streamlit dashboard on port 5000..."
streamlit run app.py --server.port 5000 --server.address 0.0.0.0 &

# Wait for Streamlit to start
sleep 5

# Install Node.js dependencies if needed
if [ -f "package.json" ]; then
    echo "Installing Node.js dependencies..."
    npm install
    
    # Start Node.js proxy server
    echo "Starting Node.js proxy server on port 3000..."
    node server.js &
fi

# Start Flask wrapper if preferred
echo "Starting Flask wrapper on port 8000..."
python main_app.py

echo "All services started!"
echo "- Streamlit: http://localhost:5000"
echo "- Flask Wrapper: http://localhost:8000" 
echo "- Node.js Proxy: http://localhost:3000"
"""
    
    with open('run_embedded.sh', 'w') as f:
        f.write(script)
    
    # Make script executable
    os.chmod('run_embedded.sh', 0o755)

if __name__ == '__main__':
    print("Setting up Smart Acquisition for embedding...")
    
    create_replit_config()
    create_package_json()
    create_node_proxy_server() 
    create_embedded_html()
    create_run_script()
    
    print("""
✅ Embedding setup complete!

You now have multiple options for embedding:

1. **Simple Iframe Embedding**:
   - Use: <iframe src="https://your-replit.replit.app" width="100%" height="800px"></iframe>

2. **Flask Wrapper** (Port 8000):
   - Run: python main_app.py
   - Professional wrapper with navigation

3. **Node.js Proxy Server** (Port 3000):
   - Run: npm install && node server.js
   - Advanced proxy with WebSocket support

4. **Multi-service Setup**:
   - Run: ./run_embedded.sh
   - All services running simultaneously

Choose the option that best fits your integration needs!
    """)