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

---

## 📦 FastAPI Backend Setup with Docker Compose & Prometheus

This project uses **Docker Compose** to orchestrate a **FastAPI backend**, a **PostgreSQL database**, and a **Prometheus monitoring service**.

---

### 🔧 Docker Compose Overview

We define three main services in the `docker-compose.yml` file:

* **`app`** – Runs the **FastAPI** application using `uvicorn`, listening on **port 8000**. It is built from a custom **Dockerfile** and depends on the database service.
* **`db`** – A **PostgreSQL** container used for persistent data storage. It is initialized with a database, user, and password.
* **`prometheus`** – A **Prometheus** container configured to monitor the `app` service. It reads from a local configuration file (`prometheus.yml`) and runs on **port 9090**.

A **named volume** is used to persist database data across container restarts. The FastAPI app and Prometheus communicate internally through service names defined in Docker Compose (e.g., `app:8000`).

---

### 🐳 FastAPI Docker Setup

The **Dockerfile** uses a lightweight **Python 3.8 Slim** base image. It:

* Installs dependencies from `requirements.txt`
* Copies application files into the container
* Optionally includes a `wait-for.sh` script to delay startup until PostgreSQL is ready
* Launches the FastAPI app with **Uvicorn**

The app is exposed on **`0.0.0.0:8000`** for accessibility inside the Docker network.

---

### 📊 Prometheus Monitoring Configuration

The **`prometheus.yml`** file tells Prometheus how and where to collect metrics. Key settings include:

* **Scrape interval:** every 15 seconds
* **Target:** the FastAPI app at `app:8000`

The FastAPI application must expose a **`/metrics` endpoint**, typically by using a library like [`prometheus_client`](https://pypi.org/project/prometheus-client/). This enables Prometheus to collect standard metrics about request counts, latencies, and more.

---

### ▶️ How to Run

To build and launch all services, simply run:

```bash
docker-compose up --build
```

Once started:

* Access the **FastAPI backend** at: [http://localhost:8000](http://localhost:8000)
* Open the **Prometheus UI** at: [http://localhost:9090](http://localhost:9090)

---

# For Local Server 

## Setup and Installation
1. Clone the repository
2. Run the Docker command : `docker compose up --build`

## Endpoints
- `GET /`: Root endpoint
- `GET /health`: Health check
- `GET /metrics`: Prometheus metrics
- `POST /products`: Create a new product. Support both Array of products and a single product.
- `GET /products`: Retrieve all products
- `GET /products/{product_id}`: Retrieve a specific product
- `PUT /products/{product_id}`: Update a product
- `DELETE /products/{product_id}`: Delete a product

---

# Metrics Documentation

This documentation focuses solely on metrics-related information and excludes deployment processes.

## 1. System Metrics

System metrics provide insights into the application’s resource consumption and runtime behavior. These metrics are collected using the `psutil` library and exposed in a Prometheus-compatible format for monitoring systems to scrape.

### 1.1 CPU Metrics

- **Metric Name**: `process_cpu_seconds_total`
  - **Type**: Counter
  - **Description**: Measures the total CPU time (in seconds) consumed by the application process since it started.
  - **Purpose**: Indicates the cumulative CPU usage, helping to identify whether the application is CPU-intensive or if CPU resources are being overutilized.
  - **Labels**: None
  - **Derived Metrics**:
    - **CPU Usage Rate**: Calculated as `rate(process_cpu_seconds_total[5m])`. This shows the rate of CPU time consumption over a 5-minute window, useful for detecting spikes in CPU demand.
    - **CPU Utilization Percentage**: Represents the percentage of available CPU resources used by the process, calculated by comparing `process_cpu_seconds_total` to total system CPU availability.

### 1.2 Memory Metrics

- **Metric Name**: `process_resident_memory_bytes`
  - **Type**: Gauge
  - **Description**: Tracks the amount of physical memory (RAM) currently used by the application process, measured in bytes.
  - **Purpose**: Monitors memory consumption to detect potential memory leaks or excessive memory usage that could impact system performance.
  - **Labels**: None
  - **Derived Metrics**:
    - **Memory Usage Trends**: Monitor `process_resident_memory_bytes` over time to identify patterns or gradual increases in memory usage.
    - **Alerting Thresholds**: Set alerts when memory usage exceeds predefined thresholds (e.g., 80% of available system memory).

- **Metric Name**: `process_virtual_memory_bytes`
  - **Type**: Gauge
  - **Description**: Tracks the total virtual memory allocated to the application process, including swapped memory, measured in bytes.
  - **Purpose**: Indicates the total memory reserved by the process, helping to assess memory allocation patterns and potential swap usage.
  - **Labels**: None
  - **Derived Metrics**:
    - **Memory Usage Trends**: Combine with `process_resident_memory_bytes` to analyze memory allocation versus actual usage.
    - **Alerting Thresholds**: Set alerts for excessive virtual memory allocation to prevent performance degradation.

### 1.3 Additional System Metrics

- **Metric Name**: `custom_process_open_fds`
  - **Type**: Gauge
  - **Description**: Tracks the number of open file descriptors used by the application process.
  - **Purpose**: Monitors file descriptor usage to detect resource leaks or situations where the process approaches system limits for open files.
  - **Labels**: None
  - **Collection**: Updated every 10 seconds (or as configured in `settings.metrics_collection_interval`).
  - **Use Case**: Set alerts for high file descriptor counts to prevent exhaustion of system resources.

- **Metric Name**: `custom_process_threads`
  - **Type**: Gauge
  - **Description**: Tracks the number of active threads in the application process.
  - **Purpose**: Monitors thread usage to identify excessive threading or concurrency issues that could impact performance.
  - **Labels**: None
  - **Collection**: Updated every 10 seconds (or as configured in `settings.metrics_collection_interval`).
  - **Use Case**: Use to detect anomalies in thread creation, such as sudden spikes indicating potential issues.

- **Metric Name**: Process Start Time and Uptime
  - **Type**: Gauge (for start time) / Calculated (for uptime)
  - **Description**: Tracks the application’s start time (via `time.time()` at process initialization) and calculates uptime as the duration since the process started.
  - **Purpose**: Provides insight into the application’s runtime duration and reliability, useful for tracking restarts or long-running processes.
  - **Labels**: None
  - **Use Case**: Monitor uptime to ensure the application remains stable over time.

- **Metric Name**: Garbage Collection Statistics
  - **Type**: Varies (typically Counter or Gauge, depending on implementation)
  - **Description**: Tracks garbage collection activity, such as the number of collections or reclaimed memory (if implemented, e.g., via Python’s `gc` module).
  - **Purpose**: Monitors memory management efficiency and garbage collection frequency to optimize performance.
  - **Labels**: None
  - **Use Case**: Analyze garbage collection frequency to identify memory-intensive operations.

## 2. HTTP Application Metrics

HTTP metrics provide comprehensive visibility into the application’s request lifecycle, including request volume, latency, and response characteristics. These metrics are implemented using the `prometheus_client` library and exposed via a Prometheus-compatible endpoint.

### 2.1 Request Volume Metrics

- **Metric Name**: `http_requests_total`
  - **Type**: Counter
  - **Description**: Counts the total number of HTTP requests processed by the application.
  - **Purpose**: Measures request volume to understand traffic patterns, load distribution, and endpoint usage.
  - **Labels**:
    - `method`: The HTTP method of the request (e.g., `GET`, `POST`, `PUT`, `DELETE`).
    - `endpoint`: The request path or route (e.g., `/data`, `/api/users`).
    - `status_code`: The HTTP response status code (e.g., `200`, `404`, `500`).
  - **Derived Metrics**:
    - **Global Request Rate**: Calculated as `rate(http_requests_total[5m])`. Shows the overall request rate per second over a 5-minute window.
    - **Per-Endpoint Request Rate**: Calculated as `rate(http_requests_total{endpoint="/data"}[5m])`. Tracks request rates for specific endpoints, useful for identifying high-traffic routes.
    - **Error Rate**: Calculated as `rate(http_requests_total{status_code=~"5.."}[5m])`. Monitors serveur error rates (e.g., 500, 502) to detect issues.

### 2.2 Request Performance Metrics

- **Metric Name**: `http_request_duration_seconds`
  - **Type**: Histogram
  - **Description**: Measures the duration of HTTP requests in seconds, organized into predefined buckets.
  - **Purpose**: Tracks request latency to identify performance bottlenecks or slow endpoints.
  - **Labels**:
    - `endpoint`: The request path or route (e.g., `/data`).
  - **Buckets**: `[0.1, 0.3, 0.5, 1.0, 2.0, 5.0, 10.0]` seconds.
  - **Derived Metrics**:
    - **95th Percentile Latency**: Calculated as `histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket{endpoint="/data",method="GET"}[5m])) by (le))`. Measures the 95th percentile latency for specific endpoints and methods, indicating the latency experienced by 95% of requests.
    - **Average Latency**: Calculated as `avg(rate(http_request_duration_seconds_sum[5m])) / avg(rate(http_request_duration_seconds_count[5m]))`. Provides the average request duration over a 5-minute window.

- **Metric Name**: Request and Response Size Histogram
  - **Type**: Histogram (if implemented)
  - **Description**: Tracks the size of HTTP requests and responses in bytes.
  - **Purpose**: Monitors payload sizes to detect unusually large requests or responses that could impact performance.
  - **Labels**: None (or specify if implemented with labels like `endpoint` or `method`).
  - **Buckets**: To be defined based on typical request/response sizes (e.g., `[100, 500, 1000, 5000, 10000]` bytes).
  - **Use Case**: Set alerts for large payloads to optimize data transfer and prevent resource exhaustion.

## 3. Monitoring and Usage Notes

- **Metrics Endpoint**: All metrics are exposed via a Prometheus-compatible endpoint (e.g., `/metrics`) for scraping by monitoring systems like Prometheus.
- **Performance Considerations**: Metrics collection is designed to maintain application performance under load. System metrics are collected at a 10-second interval (or as configured), minimizing overhead.
- **Monitoring Recommendations**:
  - Use derived metrics (e.g., rates, percentiles) in monitoring dashboards to visualize trends and set up alerts for anomalies.
  - Example Alerts:
    - High CPU usage: `rate(process_cpu_seconds_total[5m]) > 0.8`.
    - Memory usage exceeding threshold: `process_resident_memory_bytes > 0.8 * <system_memory_total>`.
    - High error rate: `rate(http_requests_total{status_code=~"5.."}[5m]) > 0.1`.
    - High latency: `histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le)) > 2`.
- **Label Usage**: Labels like `method`, `endpoint`, and `status_code` allow fine-grained analysis of HTTP metrics, enabling filtering by specific routes or response types.

---

## Monitoring Setup
1. Configure Prometheus to scrape the `/metrics` endpoint

## Configuration
Edit `app/config.py` to modify:
- Metrics collection interval
- Histogram buckets

## Fastapi Usage Example
- Create: `POST /products` with `{"id": 1, "name": "Laptop", "price": 999.99, "amount": 10}` . It supports array of Product object insert too.
- Update: `PUT /products/1` with `{"id": 1, "name": "Laptop", "price": 1099.99, "amount": 8}`
- Read: `GET /products/1` or `GET /products`
- Delete: `DELETE /products/1`

# FOR PROFESSIONALLY AWS SETUP 

----------

# 🛠️ Complete EC2 to Docker Deployment Guideline

### 🚀 From Launching Instance to Accessing FastAPI, PostgreSQL, and Prometheus

----------

## ✅ Step 1: Launch EC2 Instance on AWS

1.  Choose Image: Ubuntu 22.04 LTS  
      
    
2.  Instance Type: t2.micro (Free Tier)  
      
    
3.  Key Pair:  
      
    

-   Create new → abrarKey.pem  
      
    
-   Download and store safely  
      
    

5.  Security Group (Inbound Rules):  
    ✅ Enable:  
      
    

-   SSH (22) from anywhere  
      
    
-   HTTP (80) from anywhere  
      
    
-   HTTPS (443) from anywhere  
      
    

----------

## 🔑 Step 2: SSH Into EC2 Instance

### On your local machine (if you are using wsl then only copy using following command but if you are directly in linux ignore it and manually move it to a safe place):

```bash
cp "/mnt/c/Users/Sayedul Abrar/Downloads/abrarKey.pem" ~/

  
  

chmod 400 abrarKey.pem

  

(Optional DNS fix for ping/network)

sudo bash -c 'echo "nameserver 8.8.8.8" > /etc/resolv.conf'

  

SSH into EC2:

ssh -i "abrarKey.pem" ubuntu@<EC2_PUBLIC_DNS>

```

  

----------

## 🐳 Step 3: Install Docker and Docker Compose

# Install Docker

```bash
sudo apt update && sudo apt install -y docker.io

sudo systemctl enable docker

sudo systemctl start docker

```
  

# Add current user to docker group

```bash
sudo usermod -aG docker ubuntu

newgrp docker
```
  

### Install Docker Compose (v2)

```bash
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

sudo chmod +x /usr/local/bin/docker-compose
```
  

----------

## ✅ Step 4: Verify Docker Compose

### If docker-compose isn't found or doesn't respond:

#### A. Check file type and permissions:

```bash
file /usr/local/bin/docker-compose

ls -l /usr/local/bin/docker-compose

  

#### B. Try manually running:

/usr/local/bin/docker-compose version

  

#### C. Refresh shell cache:

# For bash

hash -r

  

# For zsh (optional)

rehash
```
  

#### D. Try again:
```bash
docker-compose version
```
  

✅ You should now see version info like:
```bash
Docker Compose version v2.x.x
```
  

----------

## 📦 Step 5: Clone Repo and Build Docker Containers

# Clone your GitHub repo
```bash
git clone https://github.com/your-username/your-repo.git

cd your-repo

  

# Run docker-compose

docker-compose up --build -d
```
  

----------

## 🌐 Step 6: Update Inbound Rules in EC2 Security Group

Go to EC2 > Instance > Security → Edit Inbound Rules and add:

| Type       | Port | Source        | Description            |
|------------|------|---------------|------------------------|
| Custom TCP | 8000 | 0.0.0.0/0     | FastAPI App            |
| Custom TCP | 9090 | 0.0.0.0/0     | Prometheus Dashboard   |
| Custom TCP | 5432 | Your IP only  | PostgreSQL (Private)   |
| HTTP       | 80   | 0.0.0.0/0     | Web traffic            |
| HTTPS      | 443  | 0.0.0.0/0     | Secure web traffic     |


----------

  
  
  

# 🔐 DockerHub Image Usage: Public vs Private

----------

  

## Create a public/private repo in docker and get the repository name  
```bash
### A. Push your image as usual (locally):

docker login

docker build -t repository name:tag .

docker push repository name:tag
```

## 1️⃣ Public Docker Image

-   You do NOT need to authenticate on the server to pull the image.  
      
    

EC2 can pull the image directly with: 

```bash  
docker-compose pull
```
-   Anyone can pull the image.  
      
    

----------

## 2️⃣ Private Docker Image

  
```bash
### B. On EC2, you must authenticate before pulling:

docker login

# Enter your DockerHub username and password or access token

  

Or use Docker Hub Access Tokens (recommended over password):

-   Create a token in DockerHub (Account Settings → Security → New Access Token)  
      
    
-   Use it as password in docker login  
      
    

### C. Edit the docker-compose file instead of “build” use  
“image: repository_name:tagname”

```  

----------

# 📁 Git Repo Best Practices for Your Dockerized App

----------

## What to include:

-   Dockerfile  
      
    
-   docker-compose.yml  
      
    
-   prometheus.yml  
      
    
-   requirements.txt (or Pipfile, poetry.lock, etc. for dependencies)  
      
    
-   Any config files needed to build and run the app  
      
    

----------

## What to exclude:

-   The whole app source folder (your application code) if:  
      
    

-   You build and push a Docker image separately to DockerHub and  
      
    
-   Your app container will run from that image (so code is baked in image)  
      
    

-   .env files or sensitive config files (use secrets or environment variables in deployment)  
      
    

### Use a .env file on the server only (don’t push it to GitHub)

-   Create a .env file on the EC2 server, e.g.:
    

SECRET_KEY=your-prod-secret

DATABASE_URL=postgresql://postgres:postgres@db:5432/product_db

-   Reference it from docker-compose.yml:
    
```yaml
services:

app:

image: your-image

env_file:

- .env
```
-   Add .env to .gitignore:
    

.env

This way, .env will never be pushed.

  

----------

### Summary:

-   If your Docker image contains the full app (built locally and pushed to DockerHub), then no need to push the app folder source to Git on your server repo.  
      
    
-   The Git repo on your server only needs the files that orchestrate the deployment (docker-compose.yml, prometheus.yml, Dockerfile if you want to build locally, requirements.txt if building locally).  
      
    

----------

# 🔄 Workflow Examples

----------

### Case A: Build & push Docker image locally → use only docker-compose.yml and prometheus.yml on EC2

-   Git repo on EC2 contains only deployment files, no app source code  
      
    
-   EC2 pulls image from DockerHub (public or private with login)  
      
    

----------

### Case B: Build image on EC2 itself (no DockerHub push)

-   Git repo must contain app source (app/ folder), Dockerfile, requirements.txt etc.  
      
    
-   EC2 runs docker-compose build locally  
      
    

----------

  

## 🌍 Step 8: Access Services from Browser

## Use your EC2 Public IP:(Access it from the EC2 server running)


-   FastAPI:  
    http://<PUBLIC_IP>:8000  
      
    
-   Prometheus:  
    http://<PUBLIC_IP>:9090  
      
    

----------
