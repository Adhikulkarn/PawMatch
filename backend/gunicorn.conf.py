"""
Production Gunicorn configuration file for PawMatch.
"""
import multiprocessing
import os

# Server socket configuration
port = os.getenv("PORT", "8000")
bind = f"0.0.0.0:{port}"

# Worker processes configuration
# Optimized for cloud starter instances (Render/ECS/Kubernetes)
workers = int(os.getenv("GUNICORN_WORKERS", "2"))
threads = int(os.getenv("GUNICORN_THREADS", "4"))
worker_class = "gthread"

# Worker lifecycle & recycling
timeout = int(os.getenv("GUNICORN_TIMEOUT", "60"))
keepalive = int(os.getenv("GUNICORN_KEEPALIVE", "5"))
max_requests = int(os.getenv("GUNICORN_MAX_REQUESTS", "1000"))
max_requests_jitter = int(os.getenv("GUNICORN_MAX_REQUESTS_JITTER", "50"))

# Logging configuration
accesslog = "-"
errorlog = "-"
loglevel = os.getenv("LOG_LEVEL", "info").lower()
capture_output = True

# Process naming
proc_name = "pawmatch_gunicorn"
