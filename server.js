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