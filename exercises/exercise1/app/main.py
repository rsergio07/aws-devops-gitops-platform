"""
SRE-Instrumented Flask Application

Production-ready microservice with comprehensive observability including:
- Prometheus metrics collection and exposition
- Structured JSON logging for automated parsing
- Kubernetes-compatible health and readiness probes
- Business logic demonstration with simulated data
"""

import json
import logging
import random
import sys
import time
from datetime import datetime
from functools import wraps

from flask import Flask, jsonify, request
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST

from app.config import Config


# Validate configuration before application startup
Config.validate()

# Initialize Flask application
app = Flask(__name__)
app.config.from_object(Config)

# Configure structured logging
logging.basicConfig(
    level=getattr(logging, Config.LOG_LEVEL.upper()),
    format='%(message)s',  # Structured logging formats messages internally
    stream=sys.stdout
)
logger = logging.getLogger(__name__)


# ============================================================================
# Prometheus Metrics Instrumentation
# ============================================================================

# HTTP Request Metrics
http_requests_total = Counter(
    'http_requests_total',
    'Total number of HTTP requests',
    ['method', 'endpoint', 'status_code']
)

http_request_duration_seconds = Histogram(
    'http_request_duration_seconds',
    'HTTP request latency in seconds',
    ['method', 'endpoint']
)

# Business Metrics
business_operations_total = Counter(
    'business_operations_total',
    'Total number of business operations',
    ['operation', 'status']
)

# Application Health Metrics
app_info = Gauge(
    'app_info',
    'Application information',
    ['app_name', 'version', 'environment']
)

app_info.labels(
    app_name=Config.APP_NAME,
    version=Config.APP_VERSION,
    environment=Config.ENVIRONMENT
).set(1)


# ============================================================================
# Structured Logging Helper
# ============================================================================

def log_structured(level, event, **kwargs):
    """
    Log structured JSON for automated parsing in log aggregation systems.
    
    Args:
        level: Log level (info, warning, error, etc.)
        event: Event type identifier
        **kwargs: Additional contextual fields
    """
    if Config.LOG_FORMAT == "json":
        log_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": level.upper(),
            "event": event,
            "app_name": Config.APP_NAME,
            "environment": Config.ENVIRONMENT,
            **kwargs
        }
        logger.log(getattr(logging, level.upper()), json.dumps(log_entry))
    else:
        # Text format for local development
        message = f"[{event}] " + " ".join(f"{k}={v}" for k, v in kwargs.items())
        logger.log(getattr(logging, level.upper()), message)


# ============================================================================
# Request Instrumentation Decorator
# ============================================================================

def instrument_request(endpoint_name):
    """
    Decorator to instrument Flask endpoints with metrics and logging.
    
    Args:
        endpoint_name: Human-readable endpoint identifier for metrics
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            start_time = time.time()
            
            # Log incoming request
            log_structured(
                "info",
                "request_received",
                method=request.method,
                path=request.path,
                remote_addr=request.remote_addr,
                user_agent=request.headers.get('User-Agent', 'unknown')
            )
            
            try:
                # Execute endpoint logic
                response = f(*args, **kwargs)
                
                # Extract status code from response
                if isinstance(response, tuple):
                    status_code = response[1] if len(response) > 1 else 200
                else:
                    status_code = 200
                
                # Record metrics
                duration = time.time() - start_time
                http_requests_total.labels(
                    method=request.method,
                    endpoint=endpoint_name,
                    status_code=status_code
                ).inc()
                http_request_duration_seconds.labels(
                    method=request.method,
                    endpoint=endpoint_name
                ).observe(duration)
                
                # Log completed request
                log_structured(
                    "info",
                    "request_completed",
                    method=request.method,
                    path=request.path,
                    status_code=status_code,
                    duration_ms=round(duration * 1000, 2)
                )
                
                return response
                
            except Exception as e:
                # Log error
                duration = time.time() - start_time
                log_structured(
                    "error",
                    "request_failed",
                    method=request.method,
                    path=request.path,
                    error=str(e),
                    duration_ms=round(duration * 1000, 2)
                )
                
                # Record error metric
                http_requests_total.labels(
                    method=request.method,
                    endpoint=endpoint_name,
                    status_code=500
                ).inc()
                
                raise
        
        return decorated_function
    return decorator


# ============================================================================
# Health Check Endpoints (Kubernetes Probes)
# ============================================================================

@app.route('/health', methods=['GET'])
@instrument_request('health_check')
def health_check():
    """
    Liveness probe endpoint for Kubernetes.
    
    Returns 200 if application is alive and should not be restarted.
    This endpoint should only fail if the application is in an unrecoverable state.
    """
    health_status = {
        "status": "healthy",
        "timestamp": time.time(),
        "version": Config.APP_VERSION,
        "checks": {
            "application": "ok",
            "memory": "ok",
            "disk": "ok"
        }
    }
    return jsonify(health_status), 200


@app.route('/ready', methods=['GET'])
@instrument_request('readiness_check')
def readiness_check():
    """
    Readiness probe endpoint for Kubernetes.
    
    Returns 200 if application is ready to serve traffic.
    Returns 503 if application is temporarily unable to serve traffic.
    
    This endpoint should check dependencies (databases, APIs, etc.) that must
    be available for the application to function correctly.
    """
    # Simulate occasional readiness failures for demonstration
    if Config.ENABLE_RANDOM_FAILURES and random.random() < (Config.FAILURE_RATE / 10):
        log_structured("warning", "readiness_check_failed", reason="simulated_failure")
        return jsonify({
            "status": "not_ready",
            "timestamp": time.time(),
            "checks": {
                "cache": "ok",
                "database": "degraded",
                "external_api": "ok"
            }
        }), 503
    
    readiness_status = {
        "status": "ready",
        "timestamp": time.time(),
        "checks": {
            "cache": "ok",
            "database": "ok",
            "external_api": "ok"
        }
    }
    return jsonify(readiness_status), 200


# ============================================================================
# Prometheus Metrics Endpoint
# ============================================================================

@app.route('/metrics', methods=['GET'])
def metrics():
    """
    Prometheus metrics exposition endpoint.
    
    Exposes all collected metrics in Prometheus text format for scraping
    by Prometheus server or compatible monitoring systems.
    """
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}


# ============================================================================
# Application Endpoints (Business Logic)
# ============================================================================

@app.route('/', methods=['GET'])
@instrument_request('home')
def home():
    """
    Home endpoint returning application information.
    """
    return jsonify({
        "message": f"Welcome to {Config.APP_NAME}!",
        "version": Config.APP_VERSION,
        "environment": Config.ENVIRONMENT,
        "status": "healthy",
        "timestamp": time.time(),
        "endpoints": {
            "health": "/health",
            "ready": "/ready",
            "metrics": "/metrics",
            "stores": "/stores"
        }
    }), 200


@app.route('/stores', methods=['GET'])
@instrument_request('get_stores')
def get_stores():
    """
    Business logic endpoint demonstrating data retrieval with observability.
    
    Simulates fetching store data with occasional failures for demonstration
    of error handling, metrics, and logging.
    """
    start_time = time.time()
    
    # Simulate occasional failures for demonstration
    if Config.ENABLE_RANDOM_FAILURES and random.random() < Config.FAILURE_RATE:
        business_operations_total.labels(
            operation='store_fetch',
            status='error'
        ).inc()
        
        log_structured(
            "warning",
            "store_fetch_failed",
            reason="simulated_service_degradation"
        )
        
        return jsonify({
            "error": "Service temporarily unavailable",
            "message": "Please try again later"
        }), 503
    
    # Simulate data retrieval
    stores_data = {
        "stores": [
            {
                "id": 1,
                "name": "AWS DevOps Store",
                "location": "us-east-1",
                "items": [
                    {"id": 1, "name": "EKS Cluster", "price": 299.99, "stock": 5},
                    {"id": 2, "name": "Terraform Module", "price": 149.99, "stock": 12},
                    {"id": 3, "name": "ArgoCD License", "price": 199.99, "stock": 8}
                ]
            },
            {
                "id": 2,
                "name": "GitOps Marketplace",
                "location": "us-west-2",
                "items": [
                    {"id": 4, "name": "CI/CD Pipeline", "price": 249.99, "stock": 15},
                    {"id": 5, "name": "Monitoring Stack", "price": 179.99, "stock": 7},
                    {"id": 6, "name": "Security Scanner", "price": 129.99, "stock": 20}
                ]
            }
        ],
        "total_stores": 2,
        "processing_time": round(time.time() - start_time, 3)
    }
    
    # Record successful business operation
    business_operations_total.labels(
        operation='store_fetch',
        status='success'
    ).inc()
    
    log_structured(
        "info",
        "store_fetch_completed",
        store_count=stores_data["total_stores"],
        processing_time=stores_data["processing_time"]
    )
    
    return jsonify(stores_data), 200


@app.route('/stores/<int:store_id>', methods=['GET'])
@instrument_request('get_store')
def get_store(store_id):
    """
    Get specific store details by ID.
    
    Demonstrates parameterized endpoints with validation and error handling.
    """
    # Simulate store lookup
    if store_id not in [1, 2]:
        log_structured(
            "warning",
            "store_not_found",
            store_id=store_id
        )
        return jsonify({
            "error": "Store not found",
            "store_id": store_id
        }), 404
    
    store_data = {
        "id": store_id,
        "name": f"Store {store_id}",
        "location": "us-east-1" if store_id == 1 else "us-west-2",
        "status": "operational"
    }
    
    business_operations_total.labels(
        operation='store_detail_fetch',
        status='success'
    ).inc()
    
    return jsonify(store_data), 200


# ============================================================================
# Error Handlers
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors with structured response."""
    log_structured(
        "info",
        "not_found",
        path=request.path,
        method=request.method
    )
    
    http_requests_total.labels(
        method=request.method,
        endpoint='unknown',
        status_code=404
    ).inc()
    
    return jsonify({
        "error": "Not found",
        "path": request.path,
        "message": "The requested resource does not exist"
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors with structured response."""
    log_structured(
        "error",
        "internal_server_error",
        path=request.path,
        method=request.method,
        error=str(error)
    )
    
    http_requests_total.labels(
        method=request.method,
        endpoint='unknown',
        status_code=500
    ).inc()
    
    return jsonify({
        "error": "Internal server error",
        "message": "An unexpected error occurred"
    }), 500


# ============================================================================
# Application Startup
# ============================================================================

if __name__ == "__main__":
    # Log application startup
    log_structured(
        "info",
        "application_starting",
        **Config.display()
    )
    
    # Start Flask application
    app.run(
        host=Config.HOST,
        port=Config.PORT,
        debug=Config.DEBUG
    )