#!/usr/bin/env bash
# ==============================================================================
# PawMatch Enterprise Render Build Script
# Hardened Deployment Automation with Error Trapping & Safety Probes
# ==============================================================================

# Strict Bash Execution Flags for Production Safety
set -o errexit
set -o pipefail
set -o nounset

# Timestamped Logger for Render Dashboard Telemetry
log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] [PAWMATCH BUILD] $1"
}

# Error Trap Handler for Failure Reporting
trap 'log "CRITICAL ERROR: Build process failed at line $LINENO with exit code $?. Check stack trace above."' ERR

log "Starting PawMatch deployment pipeline..."

# 1. Upgrade Package Manager
log "Upgrading pip package installer..."
python -m pip install --upgrade pip --quiet

# 2. Install Dependencies
log "Installing production dependencies from requirements/production.txt..."
python -m pip install -r requirements/production.txt --quiet

# 3. System & Security Validation Checks
log "Executing Django system deployment checks..."
python manage.py check --deploy

# 4. WhiteNoise Static Asset Collection
log "Collecting static assets..."
python manage.py collectstatic --noinput --clear

# 5. Database Schema Migration Safety Execution
log "Applying database schema migrations..."
python manage.py migrate --noinput

log "Deployment build pipeline completed successfully!"
