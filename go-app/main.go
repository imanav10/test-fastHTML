package main

import (
    "encoding/json"
    "fmt"
    "net/http"
    "runtime"
    "sync/atomic"
    "time"
    "html/template"

    "github.com/shirou/gopsutil/v3/cpu"
    "github.com/shirou/gopsutil/v3/mem"
)

type PageData struct {
    ServerStartTime  int64   `json:"serverStartTime"`
    RenderStartTime  int64   `json:"renderStartTime"`
    RenderEndTime    int64   `json:"renderEndTime"`
    RenderDuration   int64   `json:"renderDuration"`
    CPUUsage         float64 `json:"cpuUsage"`
    MemoryUsage      uint64  `json:"memoryUsage"`
    TotalMemory      uint64  `json:"totalMemory"`
    GoroutineCount   int     `json:"goroutineCount"`
    RequestCount     int64   `json:"requestCount"`
}

var (
    serverStartTime = time.Now().UnixNano()
    requestCount    int64
    totalMemory     uint64
)

func init() {
    memInfo, _ := mem.VirtualMemory()
    totalMemory = memInfo.Total / 1024 / 1024 // Convert to MB
}

func main() {
    http.HandleFunc("/", handleHome)
    http.HandleFunc("/api/performance", handleRequest)
    fmt.Println("Server is running on http://localhost:8080")
    http.ListenAndServe(":8080", nil)
}

func handleHome(w http.ResponseWriter, r *http.Request) {
    tmpl := `
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Performance Metrics</title>
    <script src="https://unpkg.com/htmx.org@1.6.1"></script>
</head>
<body>
    <h1>Server Performance Metrics</h1>
    <div hx-get="/api/performance" hx-trigger="load every 2s" hx-target="#performance-metrics">
        <div id="performance-metrics">
            Loading...
        </div>
    </div>
</body>
</html>
`
    w.Header().Set("Content-Type", "text/html")
    t, _ := template.New("home").Parse(tmpl)
    t.Execute(w, nil)
}

func handleRequest(w http.ResponseWriter, r *http.Request) {
    renderStart := time.Now().UnixNano()
    atomic.AddInt64(&requestCount, 1)

    cpuPercent, _ := cpu.Percent(0, false)
    memInfo, _ := mem.VirtualMemory()

    renderEnd := time.Now().UnixNano()

    data := PageData{
        ServerStartTime:  serverStartTime,
        RenderStartTime:  renderStart,
        RenderEndTime:    renderEnd,
        RenderDuration:   renderEnd - renderStart,
        CPUUsage:         cpuPercent[0],
        MemoryUsage:      memInfo.Used / 1024 / 1024, // Convert to MB
        TotalMemory:      totalMemory,
        GoroutineCount:   runtime.NumGoroutine(),
        RequestCount:     atomic.LoadInt64(&requestCount),
    }

    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(data)
}
