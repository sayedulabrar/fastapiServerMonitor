from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from ..metrics.http_metrics import http_requests_total, http_request_duration_seconds
import time

class MetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        endpoint = request.url.path
        
        try:
            response = await call_next(request)
            status_code = response.status_code
        except Exception as e:
            status_code = 500
            raise e
        finally:
            duration = time.time() - start_time
            http_requests_total.labels(
                method=request.method,
                endpoint=endpoint,
                status_code=status_code
            ).inc()
            http_request_duration_seconds.labels(endpoint=endpoint).observe(duration)
        
        return response