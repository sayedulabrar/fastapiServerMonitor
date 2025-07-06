# FastAPI Metrics Monitoring System

## Overview
This is a production-ready FastAPI application that implements system-level and application-level metrics monitoring using Prometheus format for a product management system.

## Features
- System metrics: CPU, memory, file descriptors, threads, and uptime
- HTTP metrics: request volume, latency, and status codes for product CRUD operations
- Prometheus-compatible metrics endpoint
- Custom middleware for HTTP metrics
- Background tasks for system metrics
- Docker-compatible deployment

## Project Structure
```
fastapi-metrics-app/
├── app/
│   ├── main.py
│   ├── metrics/
│   │   ├── __init__.py
│   │   ├── system_metrics.py
│   │   └── http_metrics.py
│   ├── middleware/
│   │   └── metrics_middleware.py
│   ├── routers/
│   │   ├── api.py
│   │   └── health.py
│   └── config.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## Setup and Installation
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the application:
   - Local: `uvicorn app.main:app --host 0.0.0.0 --port 8000`
   - Docker: `docker-compose up`

## Endpoints
- `GET /`: Root endpoint
- `GET /health`: Health check
- `GET /metrics`: Prometheus metrics
- `POST /products`: Create a new product
- `GET /products`: Retrieve all products
- `GET /products/{product_id}`: Retrieve a specific product
- `PUT /products/{product_id}`: Update a product
- `DELETE /products/{product_id}`: Delete a product

## Metrics
### System Metrics
- `process_cpu_seconds_total`: Total CPU time consumed
- `process_resident_memory_bytes`: Physical memory used
- `process_virtual_memory_bytes`: Virtual memory allocated
- `process_start_time_seconds`: Process uptime
- `process_open_fds`: Open file descriptors
- `process_threads`: Number of threads

### HTTP Metrics
- `http_requests_total{method, endpoint, status_code}`: Request counter
- `http_request_duration_seconds{endpoint}`: Request duration histogram

## Monitoring Setup
1. Configure Prometheus to scrape the `/metrics` endpoint
2. Use Grafana for visualization (optional)
3. Set up alerts based on metrics thresholds

## Configuration
Edit `app/config.py` to modify:
- Metrics collection interval
- Histogram buckets

## Usage Example
- Create: `POST /products` with `{"id": 1, "name": "Laptop", "price": 999.99, "amount": 10}`
- Update: `PUT /products/1` with `{"id": 1, "name": "Laptop", "price": 1099.99, "amount": 8}`
- Read: `GET /products/1` or `GET /products`
- Delete: `DELETE /products/1`