#!/usr/bin/env python3
"""
Main application launcher that can run multiple services
This allows you to embed the Streamlit dashboard with other apps
"""

import subprocess
import threading
import time
import os
from flask import Flask, render_template_string

# Flask app for the main interface
app = Flask(__name__)

# HTML template that embeds the Streamlit app
MAIN_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Smart Acquisition - Integrated Dashboard</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            font-family: Arial, sans-serif;
            background-color: #f0f0f0;
        }
        .header {
            background-color: #2c3e50;
            color: white;
            padding: 1rem;
            text-align: center;
        }
        .nav {
            background-color: #34495e;
            padding: 0.5rem;
            text-align: center;
        }
        .nav a {
            color: white;
            text-decoration: none;
            margin: 0 1rem;
            padding: 0.5rem 1rem;
            border-radius: 4px;
            background-color: #2c3e50;
        }
        .nav a:hover {
            background-color: #1a252f;
        }
        .content {
            height: calc(100vh - 120px);
        }
        iframe {
            width: 100%;
            height: 100%;
            border: none;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>Smart Acquisition - Integrated Platform</h1>
    </div>
    <div class="nav">
        <a href="#" onclick="showDashboard()">Market Intelligence Dashboard</a>
        <a href="#" onclick="showOtherApp()">Other App</a>
        <a href="#" onclick="showAPI()">API Documentation</a>
    </div>
    <div class="content">
        <iframe id="mainFrame" src="http://localhost:5000"></iframe>
    </div>

    <script>
        function showDashboard() {
            document.getElementById('mainFrame').src = 'http://localhost:5000';
        }
        
        function showOtherApp() {
            // You can point this to another service running on a different port
            document.getElementById('mainFrame').src = 'http://localhost:3000';
        }
        
        function showAPI() {
            // Or show API documentation
            document.getElementById('mainFrame').src = '/api-docs';
        }
    </script>
</body>
</html>
"""

@app.route('/')
def main_dashboard():
    return render_template_string(MAIN_TEMPLATE)

@app.route('/api-docs')
def api_docs():
    return """
    <h1>Smart Acquisition API Documentation</h1>
    <p>This would contain your API documentation or other content</p>
    <p>You can embed any other application or content here</p>
    """

def run_streamlit():
    """Run the Streamlit app on port 5000"""
    subprocess.run(['streamlit', 'run', 'app.py', '--server.port', '5000', '--server.address', '0.0.0.0'])

def run_flask():
    """Run the Flask wrapper on port 8000"""
    app.run(host='0.0.0.0', port=8000, debug=False)

if __name__ == '__main__':
    # Start Streamlit in a separate thread
    streamlit_thread = threading.Thread(target=run_streamlit)
    streamlit_thread.daemon = True
    streamlit_thread.start()
    
    # Wait a moment for Streamlit to start
    time.sleep(3)
    
    print("Starting integrated dashboard...")
    print("- Streamlit Dashboard: http://localhost:5000")
    print("- Main Interface: http://localhost:8000")
    
    # Start Flask
    run_flask()