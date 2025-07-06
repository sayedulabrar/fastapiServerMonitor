from fastapi import FastAPI
from prometheus_client import make_asgi_app
import asyncio
from .middleware.metrics_middleware import MetricsMiddleware
from .routers import api, health
from .metrics.system_metrics import collect_system_metrics
from .config import settings # Configuration settings like metrics collection interval. 
from .database import engine
from . import models



models.Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(title="FastAPI Metrics Monitoring System")

# Mount Prometheus metrics endpoint
# make_asgi_app() returns an ASGI application that exposes metrics in Prometheus-compatible format.
# It creates a mini web app that knows how to serve Prometheus data when hit. MetricsMiddleware (or any FastAPI middleware) does not run for it.
prometheus_app = make_asgi_app()
app.mount("/metrics", prometheus_app)

# Add middleware and routers
app.add_middleware(MetricsMiddleware) # Custom middleware for tracking HTTP metrics. for this app's routes.
app.include_router(api.router) # Routers for product CRUD operations 
app.include_router(health.router) # Router for health check endpoint


# asyncio: Used for running background tasks asynchronously. When the app boots up, start collecting system metrics in the background.
@app.on_event("startup")
async def startup_event():
    """Start background metrics collection task"""
    asyncio.create_task(collect_system_metrics())

@app.get("/")
async def root():
    return {"message": "FastAPI Metrics Monitoring System"}