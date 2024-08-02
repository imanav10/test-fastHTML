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
    text1 = Container(P("In the ever-evolving world of web development, choosing the right server-side language is crucial for optimizing performance and scalability. This blog post delves into the performance characteristics of JavaScript (Node.js), Go, and Python, three popular languages used for server-side programming. We are making a performance dashboard which shows loading/response time for that webpage. We'll be doing this experiment by using 3 language server side (GO, JS, FastHTML). Let's start by creating a React file."))
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
    text4 = Container(P("Server.js"))
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
    text10 = Container(P("JavaScript, with its runtime environment Node.js - react, has become a powerful tool for server-side development. Node.js utilizes an event-driven, non-blocking I/O model, making it lightweight and efficient. Here we'll be creating two files App.js for frontend and Server.js for Backend, to run Node server."))
    text6 = Container(P("Now we'll be creating go webserver"))
    heading3 = Container(H1("GO"))
    text11 = Container(P("Go, or Golang, developed by Google, is known for its simplicity and high performance. It is designed to be efficient in terms of memory and processing, making it a strong candidate for concurrent programming. We'll be creating a main.go file."))
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

    texto1 = Titled(Card("Output"))
    img2 = Container(Img(src='./images/react.png'))
    img3 = Container(Img(src='./images/GO.png'))
    img4 = Container(Img(src='./images/fasthtml.png'))
    texto4 = Titled(Card("Performance Benchmarks"))
    texto5= Container(H2("Response Time"))
    texto6 = Container(P("When it comes to response time, Go often outperforms Node.js and Python due to its compiled nature and efficient garbage collection. Node.js comes next with its event-driven model, followed by Python, which can lag behind due to its interpreted nature. We got same output here."))
    texto7 = Container(H2("Concurrency Handling"))
    texto8 = Container(P("Go's goroutines provide an efficient way to handle thousands of concurrent tasks with minimal overhead. Node.js also handles concurrency well with its asynchronous callbacks and promises, but it can struggle with CPU-bound tasks. Python, while capable of concurrency through libraries like asyncio, is generally slower in this aspect."))
    texto9 = Container(H2("Memory Usage"))
    texto10 = Container(P(("Go is designed to be memory efficient, often consuming less memory than Node.js and Python for similar tasks. Node.js, while more memory-efficient than Python, can still be heavy on memory due to its single-threaded nature and reliance on external libraries. Python tends to use more memory, especially when running multiple processes.")))
    txt1 = Container(Li("JavaScript Engine: Node.js runs on the V8 engine, which is designed for high performance and includes just-in-time (JIT) compilation. This can sometimes result in higher memory usage due to the overhead of JIT compilation and the optimizations performed by the V8 engine."),Li("Event Loop: Node.js operates on a single-threaded event loop. While this is efficient for I/O-bound operations, it can consume more memory if many asynchronous callbacks are pending."))
    txt2 = Container(H4("React"))
    txt3 = Container(H4("FastHTML"))
    txt4 = Container(Li("Interpreter: Python uses an interpreter (CPython) which typically has a lower memory footprint compared to JIT compilers like V8. This is because Python executes code more straightforwardly without the overhead of JIT compilation."),Li("Concurrency Model: The provided Python script uses asyncio for handling asynchronous tasks, which can be more memory-efficient for certain types of workloads."))
    txt5 = Container(P("Here we can observe some obvious difference from our General Conclusion, python is taking less memory usage than react, this might be because :"))
    txt6 = Container(H2("Cpu usage"))
    txt7 = Container(P("CPU usage is a critical metric for understanding how efficiently a server-side language utilizes processing resources. Efficient CPU usage can lead to better performance and lower operational costs, especially under high load."))
    txt8 = Container(H4("JavaScript (Node.js)"))
    txt9 = Container(P("Node.js operates on a single-threaded event loop, which makes it highly efficient for I/O-bound tasks but can be a limitation for CPU-bound operations. Node.js relies on asynchronous programming and non-blocking I/O, which helps in keeping the CPU usage relatively low for I/O-bound tasks. However, when it comes to CPU-intensive tasks, Node.js may struggle because it doesn't natively support multi-threading in the same way as Go or Python."))
    t1 = Container(H4("GO"))
    t2 = Container(P("Go, designed with concurrency in mind, handles CPU usage exceptionally well. It uses goroutines, which are lightweight threads managed by the Go runtime. This allows Go to perform concurrent tasks efficiently with low overhead. Goroutines can scale across multiple CPU cores, making Go particularly well-suited for CPU-bound tasks."))
    t3 = Container(H4("FastHTML"))
    t4 = Container(P("Python's CPU usage can vary significantly depending on the specific implementation and libraries used. Python's Global Interpreter Lock (GIL) can be a bottleneck for CPU-bound tasks, as it allows only one thread to execute at a time. However, Python's multiprocessing module can help mitigate this by running separate processes. For I/O-bound tasks, Python's asyncio library can be efficient, similar to Node.js's event-driven model."))

    texto2 = Titled(Card("Conclusion"))
    texto3 = Container(P(("Being honest"),A("FastHTML"),(" got great code efficiency, it required less amount of code as compaired to both JS and GO. But its not all about code efficiency, based on render time, CPU usage as well as memory usage JS and GO perform much better than FastHTML.CPU usage is a crucial consideration when choosing a server-side language. Go generally offers the best performance for both I/O-bound and CPU-bound tasks due to its efficient concurrency model. Node.js is highly efficient for I/O-bound tasks but can struggle with CPU-bound operations. Python is versatile and easy to use, with good performance for I/O-bound tasks, but may require additional tuning for CPU-bound tasks due to the GIL.")))
    t5 = Container(P("Inshort choosing the right server-side language depends on the specific needs of your project. If performance and concurrency are your top priorities, Go might be the best choice. For real-time applications and a vast ecosystem, Node.js is a strong contender. If rapid development and a rich set of libraries are your main focus, Python could be the way to go."))


    l1 = Container(Ul(Li("Go: 0.33ms"),Li("React: 10ms"),Li("Python: 110ms")))
    l2 = Container(Ul(Li("Go Routine Count: 3"),Li("Python Thread Count: 2")))
    l3 = Container(Ul(Li("Go: 51.1%"),Li("React: 65.5%"),Li("Python: 52.77%")))
    l4 = Container(Ul(Li("Go: 3.44%"),Li("React: 0.49%"),Li("Python: 8.4%")))
    footer = Container(P(("Connect"),(A("x.com" ,href='https://x.com/chikoshit')),(A("github.com",href='https://github.com/imanav10'))))
    resources = Container(P("Resources: https://github.com/fasthtml, https://docs.fastht.ml/api/xtend.html,https://docs.fastht.ml/, https://go.dev/doc/,https://docs.python.org/3/"))

    return Div(Titled(" "),Div(cls="chat-header"),title,img,gap,heading, text1,heading2,text10,text3,text2,text4,text5 ,heading3,text11 ,text6,text7,heading4,text8,text9,texto4,texto5,texto6,l1,texto7,texto8,l2,texto9,texto10,l3,txt5,txt2,txt1,gap,txt3,txt4,gap,txt6,txt7,txt8,txt9,t1,t2,t3,t4,l4,texto2,texto3,t5,gap,resources,footer,hx_get="/change")


serve()