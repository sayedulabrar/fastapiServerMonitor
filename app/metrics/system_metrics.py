import psutil
import time
import asyncio
from prometheus_client import Gauge

# Custom metrics only — avoid default Prometheus metric names
file_descriptors_custom = Gauge('custom_process_open_fds', 'Number of open file descriptors')
thread_count_custom = Gauge('custom_process_threads', 'Number of threads')

process_start_time = time.time()

async def collect_system_metrics():
    process = psutil.Process()
    while True:
        try:
            file_descriptors_custom.set(process.num_fds())
            thread_count_custom.set(process.num_threads())
            await asyncio.sleep(10)  # or your settings.metrics_collection_interval
        except Exception as e:
            print(f"Error collecting system metrics: {e}")
            await asyncio.sleep(10)
