# =============================================================================
# Multi-Stage Dockerfile for Production Python Application
# =============================================================================
# This Dockerfile implements security best practices including:
# - Multi-stage builds to minimize image size
# - Non-root user execution
# - Minimal base image (python:3.11-slim)
# - No unnecessary build tools in final image
# - Health checks for container orchestration
# =============================================================================

# -----------------------------------------------------------------------------
# Stage 1: Builder
# Purpose: Install dependencies and compile packages requiring build tools
# -----------------------------------------------------------------------------
FROM python:3.11-slim AS builder

# Set working directory for build stage
WORKDIR /build

# Install system dependencies required for building Python packages
# These include compilers and headers needed for native extensions
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies to user site-packages
# --user flag installs to ~/.local which we'll copy to production stage
# --no-warn-script-location suppresses warnings about script locations
RUN pip install --user --no-cache-dir --no-warn-script-location -r requirements.txt

# -----------------------------------------------------------------------------
# Stage 2: Production
# Purpose: Minimal runtime image with only necessary dependencies
# -----------------------------------------------------------------------------
FROM python:3.11-slim

# Create non-root user for security
# - appuser: username for the application user
# - UID 1000: standard non-root user ID
# - No login shell, no home directory creation initially
RUN groupadd -r appuser && \
    useradd -r -g appuser -u 1000 -m -s /bin/false appuser

# Set working directory
WORKDIR /app

# Copy Python dependencies from builder stage
# Copy to appuser's home directory to maintain proper ownership
COPY --from=builder --chown=appuser:appuser /root/.local /home/appuser/.local

# Copy application code with proper ownership
COPY --chown=appuser:appuser app/ /app/app/

# Update PATH to include user site-packages
ENV PATH=/home/appuser/.local/bin:$PATH \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Switch to non-root user
USER appuser

# Expose application port
EXPOSE 8080

# Health check for container orchestration
# Checks /health endpoint every 30 seconds
# Container is unhealthy after 3 consecutive failures
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/health')" || exit 1

# Container entry point
# Using ENTRYPOINT instead of CMD for better signal handling
ENTRYPOINT ["python", "-m", "app.main"]

# Labels for metadata (following OCI image spec)
LABEL maintainer="AWS DevOps GitOps Platform" \
      version="1.0.0" \
      description="SRE-instrumented Flask application with Prometheus metrics" \
      org.opencontainers.image.source="https://github.com/YOUR_ORG/aws-devops-gitops-platform" \
      org.opencontainers.image.licenses="MIT"