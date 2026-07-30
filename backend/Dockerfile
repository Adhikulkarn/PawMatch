# ==============================================================================
# PawMatch Backend Production Dockerfile
# Cloud-Agnostic, Multi-Stage OCI Production Image
# ==============================================================================

# Stage 1: Build Dependencies Stage
FROM python:3.13-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install OS build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install production requirements
COPY requirements/ /app/requirements/
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements/production.txt

# Stage 2: Production Execution Stage
FROM python:3.13-slim AS runner

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000 \
    DJANGO_SETTINGS_MODULE=config.settings.production

WORKDIR /app

# Install runtime OS dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy python packages from builder stage
COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application source code
COPY . /app/

# Collect static files during build using a build dummy key
RUN SECRET_KEY="build-time-dummy-secret-key-for-collectstatic" \
    DEBUG=False \
    ALLOWED_HOSTS="*" \
    python manage.py collectstatic --noinput

# Expose backend port
EXPOSE 8000

# Container Healthcheck probe
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/health/ || exit 1

# Launch Gunicorn server using production configuration
CMD ["gunicorn", "-c", "gunicorn.conf.py", "config.wsgi:application"]
