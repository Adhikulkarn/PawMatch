"""
Production Gunicorn Configuration for PawMatch Backend API.

Dynamically configures Gunicorn workers, threads, timeouts, memory recycling,
preloading, and structured logging for cloud PaaS (Render, AWS ECS, K8s).
"""

import multiprocessing
import os

# ------------------------------------------------------------------------------
# Server Socket Configuration
# ------------------------------------------------------------------------------
port = os.getenv("PORT", "8000")
bind = f"0.0.0.0:{port}"

# ------------------------------------------------------------------------------
# Worker Processes Auto-Scaling Strategy
# ------------------------------------------------------------------------------
# Dynamic core calculation: (cpu_count * 2) + 1, with GUNICORN_WORKERS override
cpu_cores = multiprocessing.cpu_count()
default_workers = (cpu_cores * 2) + 1
workers = int(os.getenv("GUNICORN_WORKERS", str(default_workers)))

# Asynchronous Threaded Worker Configuration
worker_class = os.getenv("GUNICORN_WORKER_CLASS", "gthread")
threads = int(os.getenv("GUNICORN_THREADS", "4"))

# Application Code Preloading (reduces RAM usage across workers via Copy-On-Write)
preload_app = os.getenv("GUNICORN_PRELOAD_APP", "True").lower() in ("true", "1", "yes")

# ------------------------------------------------------------------------------
# Worker Lifecycle & Memory Recycling
# ------------------------------------------------------------------------------
timeout = int(os.getenv("GUNICORN_TIMEOUT", "60"))
keepalive = int(os.getenv("GUNICORN_KEEPALIVE", "5"))
graceful_timeout = int(os.getenv("GUNICORN_GRACEFUL_TIMEOUT", "30"))

# Worker process auto-restart limits to prevent cumulative memory leaks
max_requests = int(os.getenv("GUNICORN_MAX_REQUESTS", "1000"))
max_requests_jitter = int(os.getenv("GUNICORN_MAX_REQUESTS_JITTER", "50"))

# ------------------------------------------------------------------------------
# Logging & Observability
# ------------------------------------------------------------------------------
accesslog = "-"
errorlog = "-"
loglevel = os.getenv("LOG_LEVEL", "info").lower()
capture_output = True

# Structured Access Log Format
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(L)ss'

# Process Identifier Name
proc_name = "pawmatch_gunicorn"
