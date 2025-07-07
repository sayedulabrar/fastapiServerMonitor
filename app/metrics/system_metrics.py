import psutil
import time
import asyncio
from prometheus_client import Gauge

# Custom metrics only — avoid default Prometheus metric names
file_descriptors_custom = Gauge('custom_process_open_fds', 'Number of open file descriptors')
thread_count_custom = Gauge('custom_process_threads', 'Number of threads')
cpu_utilization_custom = Gauge('custom_cpu_utilization_percentage', 'CPU usage percentage of the process')

process_start_time = time.time()

async def collect_system_metrics():
    process = psutil.Process()
    num_cpus = psutil.cpu_count(logical=True)
    if num_cpus is None or num_cpus == 0:
        raise RuntimeError("Unable to determine the number of CPUs.")

    prev_cpu_time = process.cpu_times().user + process.cpu_times().system
    prev_time = time.time()
    while True:
        try:
            # File descriptors and thread count
            file_descriptors_custom.set(process.num_fds())
            thread_count_custom.set(process.num_threads())

            # CPU usage calculation
            current_cpu_time = process.cpu_times().user + process.cpu_times().system
            current_time = time.time()

            cpu_time_delta = current_cpu_time - prev_cpu_time
            time_delta = current_time - prev_time

            # CPU usage as a percentage of total CPU capacity
            cpu_percent = (cpu_time_delta / (time_delta * num_cpus))*100.0
            cpu_utilization_custom.set(cpu_percent)

            # Update previous values
            prev_cpu_time = current_cpu_time
            prev_time = current_time

            await asyncio.sleep(10)

        except Exception as e:
            print(f"Error collecting system metrics: {e}")
            await asyncio.sleep(10)

