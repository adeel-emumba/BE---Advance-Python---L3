# Multi-stage build for smaller image size
FROM python:3.12-slim as builder

# Set working directory
WORKDIR /app

# Install build dependencies
RUN pip install --upgrade pip setuptools wheel build

# Copy project files
COPY pyproject.toml README.md ./
COPY src/ src/

# Build the wheel
RUN python -m build --wheel

# Final stage
FROM python:3.12-slim

WORKDIR /app

# Copy only the wheel from builder
COPY --from=builder /app/dist/*.whl /app/

# Install the package
RUN pip install --no-cache-dir /app/*.whl && rm /app/*.whl

# Create non-root user for security
RUN useradd -m -u 1000 webperf && chown -R webperf:webperf /app
USER webperf

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import webperf; print('OK')" || exit 1

# Default command for CLI
ENTRYPOINT ["webperf"]

# Usage examples:
# docker build -t webperf:latest .
# docker run --rm webperf:latest --help
# docker run --rm -v $(pwd)/urls.json:/app/urls.json webperf:latest --input /app/urls.json