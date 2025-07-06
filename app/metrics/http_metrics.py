from prometheus_client import Counter, Histogram

# HTTP metrics
http_requests_total = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint', 'status_code'])
http_request_duration_seconds = Histogram(
    'http_request_duration_seconds', 
    'Request duration in seconds', 
    ['endpoint'],
    buckets=[0.1, 0.3, 0.5, 1.0, 2.0, 5.0, 10.0]
)