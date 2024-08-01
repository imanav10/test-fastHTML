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
    diction.setdefault("render_start_time", []).append(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(render_start)))
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
    return (H1("Python Performance Metrics"), Grid(data))

serve()