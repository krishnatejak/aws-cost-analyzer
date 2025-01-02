FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN useradd -m -r appuser && \
    chown -R appuser:appuser /app

USER appuser

ENV PYTHONPATH=/app
ENV AWS_DEFAULT_REGION=ap-south-1
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=wsgi.py

EXPOSE 5000

CMD ["python", "wsgi.py"]