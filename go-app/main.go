package main

import (
	"fmt"
	"html/template"
	"net/http"
	"runtime"
	"time"

	"github.com/shirou/gopsutil/v3/cpu"
	"github.com/shirou/gopsutil/v3/mem"
)

type PageData struct {
	ServerStartTime  time.Time
	RenderStartTime  time.Time
	RenderEndTime    time.Time
	RenderDuration   time.Duration
	CPUUsage         float64
	MemoryUsage      uint64
	TotalMemory      uint64
	GoroutineCount   int
	RequestCount     int
}

var (
	serverStartTime time.Time
	requestCount    int
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
        <tr><td>Page Render Duration</td><td>{{.RenderDuration}}</td></tr>
        <tr><td>CPU Usage</td><td>{{printf "%.2f%%" .CPUUsage}}</td></tr>
        <tr><td>Memory Usage</td><td>{{.MemoryUsage}} / {{.TotalMemory}} MB</td></tr>
        <tr><td>Goroutine Count</td><td>{{.GoroutineCount}}</td></tr>
        <tr><td>Total Requests Handled</td><td>{{.RequestCount}}</td></tr>
    </table>
</body>
</html>
`

func main() {
	serverStartTime = time.Now()

	http.HandleFunc("/", handleRequest)
	fmt.Println("Server is running on http://localhost:8080")
	http.ListenAndServe(":8080", nil)
}

func handleRequest(w http.ResponseWriter, r *http.Request) {
	renderStart := time.Now()
	requestCount++

	cpuPercent, _ := cpu.Percent(time.Second, false)
	memInfo, _ := mem.VirtualMemory()

	data := PageData{
		ServerStartTime:  serverStartTime,
		RenderStartTime:  renderStart,
		CPUUsage:         cpuPercent[0],
		MemoryUsage:      memInfo.Used / 1024 / 1024, // Convert to MB
		TotalMemory:      memInfo.Total / 1024 / 1024, // Convert to MB
		GoroutineCount:   runtime.NumGoroutine(),
		RequestCount:     requestCount,
	}

	tmpl, err := template.New("performance").Parse(htmlTemplate)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	renderEnd := time.Now()
	data.RenderEndTime = renderEnd
	data.RenderDuration = renderEnd.Sub(renderStart)

	err = tmpl.Execute(w, data)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
	}
}