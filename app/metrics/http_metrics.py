from prometheus_client import Counter, Histogram
from app.config import settings

# HTTP metrics
http_requests_total = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint', 'status_code'])
http_request_duration_seconds = Histogram(
    'http_request_duration_seconds', 
    'Request duration in seconds', 
    ['endpoint'],
    buckets=settings.histogram_buckets
)

http_request_size_bytes = Histogram(
    'http_request_size_bytes',
    'Size of incoming HTTP requests in bytes',
    ['endpoint'],
    buckets=settings.BYTES_BUCKETS
)

http_response_size_bytes = Histogram(
    'http_response_size_bytes',
    'Size of outgoing HTTP responses in bytes',
    ['endpoint'],
    buckets=settings.BYTES_BUCKETS
)
