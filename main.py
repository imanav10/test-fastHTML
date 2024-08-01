from fasthtml.common import *

app,rt = fast_app()
# Loading tailwind and daisyui
chat_headers = [Script(src="https://cdn.tailwindcss.com"),
           Link(rel="stylesheet", href="https://cdn.jsdelivr.net/npm/daisyui@4.11.1/dist/full.min.css")]
@rt('/')
def get():
    
    title = Div(Titled(Card('Indepth performance comparison for React vs FastHTML vs GO (Server Side)')))
    img = Container(Img(cls=f"h-0.5", src='./images/banner.png'))
    gap = Br(" ")

    heading = Titled(Card("What we are making?"))
    text1 = Container(P("We are making a performance dashboard which shows loading/response time for that webpage. We'll be doing this experiment by using 3 language server side (GO, JS, FastHTML). Let's start by creating a React file."))
    heading2 = Container(H1("React"))
    text3 = Container(P("App.js"))

    text2 = Container(Textarea(
"""// App.js
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

export default App""" ,rows= '68'
))
    text4 = Container(P("Script.js"))
    text5 = Container(Textarea(
        """
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
  const renderDuration = renderEndTime - renderStartTime ;

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
""", rows='44'
    ))
    text6 = Container(P("Now we'll be creating go webserver"))
    heading3 = Container(H1("GO"))
    text7 = Container(Textarea(

    """
package main

import (
    "fmt"
    "html/template"
    "net/http"
    "runtime"
    "sync"
    "sync/atomic"
    "time"

    "github.com/shirou/gopsutil/v3/cpu"
    "github.com/shirou/gopsutil/v3/mem"
)

type PageData struct {
    ServerStartTime  time.Time
    RenderStartTime  time.Time
    RenderEndTime    time.Time
    RenderDuration   float64 // Changed to float64 for milliseconds
    CPUUsage         float64
    MemoryUsage      uint64
    TotalMemory      uint64
    GoroutineCount   int
    RequestCount     int
}

var (
    serverStartTime time.Time
    requestCount    int64
    mu              sync.Mutex
    tmpl            *template.Template
)

const htmlTemplate = `
<!DOCTYPE html>
<html>
<head>
    <title>Go Performance Metrics</title>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; padding: 20px; }
        h1 { color: #333; }
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
    </style>
</head>
<body>
    <h1>Go Performance Metrics</h1>
    <table>
        <tr><th>Metric</th><th>Value</th></tr>
        <tr><td>Server Start Time</td><td>{{.ServerStartTime}}</td></tr>
        <tr><td>Page Render Start Time</td><td>{{.RenderStartTime}}</td></tr>
        <tr><td>Page Render End Time</td><td>{{.RenderEndTime}}</td></tr>
        <tr><td>Page Render Duration</td><td>{{printf "%.2f ms" .RenderDuration}}</td></tr>
        <tr><td>CPU Usage</td><td>{{printf "%.2f%%" .CPUUsage}}</td></tr>
        <tr><td>Memory Usage</td><td>{{.MemoryUsage}} / {{.TotalMemory}} MB</td></tr>
        <tr><td>Goroutine Count</td><td>{{.GoroutineCount}}</td></tr>
        <tr><td>Total Requests Handled</td><td>{{.RequestCount}}</td></tr>
    </table>
</body>
</html>
`

func init() {
    var err error
    tmpl, err = template.New("performance").Parse(htmlTemplate)
    if err != nil {
        panic(err)
    }
}

func main() {
    serverStartTime = time.Now()
    http.HandleFunc("/", handleRequest)
    fmt.Println("Server is running on http://localhost:8080")
    http.ListenAndServe(":8080", nil)
}

func handleRequest(w http.ResponseWriter, r *http.Request) {
    renderStart := time.Now()
    atomic.AddInt64(&requestCount, 1)

    cpuPercent, _ := cpu.Percent(0, false)
    memInfo, _ := mem.VirtualMemory()

    renderEnd := time.Now()
    renderDuration := float64(renderEnd.Sub(renderStart).Microseconds()) / 1000 // Convert to milliseconds

    data := PageData{
        ServerStartTime:  serverStartTime,
        RenderStartTime:  renderStart,
        RenderEndTime:    renderEnd,
        RenderDuration:   renderDuration,
        CPUUsage:         cpuPercent[0],
        MemoryUsage:      memInfo.Used / 1024 / 1024, // Convert to MB
        TotalMemory:      memInfo.Total / 1024 / 1024, // Convert to MB
        GoroutineCount:   runtime.NumGoroutine(),
        RequestCount:     int(atomic.LoadInt64(&requestCount)),
    }

    mu.Lock()
    err := tmpl.Execute(w, data)
    mu.Unlock()

    if err != nil {
        http.Error(w, err.Error(), http.StatusInternalServerError)
    }
}
""", rows= '109'
    ))
    heading4 = Container(H1("FastHTML"))
    text8 = Container(P("Creating FastHTML server"))
    text9 = Container(Textarea(
        """
from fasthtml.common import *
import time
import psutil
import asyncio


app = FastHTML()
rt = app.route
server_start_time = time.time()
request_count = 0

async def Gridn():
    diction = {}
    global request_count
    request_count += 1

    render_start = time.time()
    
    # Simulate some work
    await asyncio.sleep(0.01)
    
    cpu_percent = psutil.cpu_percent(interval=0.1)
    memory = psutil.virtual_memory()
    
    render_end = time.time()
    render_duration = (render_end - render_start) * 1000
    
    Thead(diction.setdefault("render_start_time", []).append(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(render_start))))
    diction.setdefault("render_end_time", []).append(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(render_end)))
    diction.setdefault("render_duration", []).append(render_duration)
    diction.setdefault("cpu_usage", []).append(cpu_percent)
    diction.setdefault("memory_usage", []).append(memory.used // (1024 * 1024))   
    diction.setdefault("total_memory", []).append(memory.total // (1024 * 1024))   
    diction.setdefault("thread_count", []).append(psutil.Process().num_threads()) 
    diction.setdefault("request_count", []).append(request_count)
    diction.setdefault("server_start_time", []).append(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(server_start_time)))

    return diction

@rt('/')
async def get():
    data = await Gridn()
    return (H1("Python Performance Metrics"), P(data))

serve()
""", rows='45'
    ))
    return Div(Titled(" "),Div(cls="chat-header"),title,img,gap,heading, text1,heading2,text3,text2,text4,text5 ,heading3,text6,text7,heading4,text8,text9,hx_get="/change")


serve()