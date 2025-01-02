# Build stage
FROM python:3.11-slim AS builder

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Production stage
FROM python:3.11-slim

COPY --from=builder /opt/venv /opt/venv

WORKDIR /app

RUN useradd -m -r appuser && \
    chown -R appuser:appuser /app

ENV PATH="/opt/venv/bin:$PATH"
ENV AWS_DEFAULT_REGION=ap-south-1
ENV PYTHONUNBUFFERED=1

COPY --chown=appuser:appuser . .

USER appuser

EXPOSE 5000

HEALTHCHECK CMD curl --fail http://localhost:5000/health || exit 1

CMD ["gunicorn", \
     "--bind", "0.0.0.0:5000", \
     "--workers", "4", \
     "--threads", "2", \
     "--worker-class", "gevent", \
     "--worker-tmp-dir", "/dev/shm", \
     "--access-logfile", "-", \
     "--error-logfile", "-", \
     "app:app"]