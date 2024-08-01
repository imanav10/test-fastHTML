// App.js
import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [performanceData, setPerformanceData] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      const response = await fetch('/api/performance');
      const data = await response.json();
      setPerformanceData(data);
    };

    fetchData();
    const interval = setInterval(fetchData, 5000); // Update every 5 seconds

    return () => clearInterval(interval);
  }, []);

  if (!performanceData) return <div>Loading...</div>;

  return (
    <div className="App">
      <h1>React Performance Metrics</h1>
      <table>
        <thead>
          <tr>
            <th>Metric</th>
            <th>Value</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Server Start Time</td>
            <td>{new Date(performanceData.serverStartTime).toLocaleString()}</td>
          </tr>
          <tr>
            <td>Page Render Start Time</td>
            <td>{new Date(performanceData.renderStartTime).toLocaleString()}</td>
          </tr>
          <tr>
            <td>Page Render End Time</td>
            <td>{new Date(performanceData.renderEndTime).toLocaleString()}</td>
          </tr>
          <tr>
            <td>Page Render Duration</td>
            <td>{performanceData.renderDuration} ms</td>
          </tr>
          <tr>
            <td>CPU Usage</td>
            <td>{performanceData.cpuUsage.toFixed(2)}%</td>
          </tr>
          <tr>
            <td>Memory Usage</td>
            <td>{performanceData.memoryUsage} / {performanceData.totalMemory} MB</td>
          </tr>
          <tr>
            <td>Request Count</td>
            <td>{performanceData.requestCount}</td>
          </tr>
        </tbody>
      </table>
    </div>
  );
}

export default App