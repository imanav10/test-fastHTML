// server.js
const express = require('express');
const os = require('os');

const app = express();
const port = 3000;

let serverStartTime = new Date();
let requestCount = 0;

app.get('/api/performance', (req, res) => {
  requestCount++;
  
  const renderStartTime = new Date();
  
  // Simulate some work
  let result = 0;
  for (let i = 0; i < 1000000; i++) {
    result += Math.random();
  }

  const renderEndTime = new Date();
  const renderDuration = renderEndTime - renderStartTime;

  const cpuUsage = os.loadavg()[0]; // 1 minute load average
  const totalMemory = os.totalmem() / (1024 * 1024); // Convert to MB
  const freeMemory = os.freemem() / (1024 * 1024); // Convert to MB
  const usedMemory = totalMemory - freeMemory;

  res.json({
    serverStartTime: serverStartTime.toISOString(),
    renderStartTime: renderStartTime.toISOString(),
    renderEndTime: renderEndTime.toISOString(),
    renderDuration,
    cpuUsage,
    memoryUsage: Math.round(usedMemory),
    totalMemory: Math.round(totalMemory),
    requestCount
  });
});

app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});