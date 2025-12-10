# Stage 1: Builder
FROM python:3.11-slim AS builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim

ENV TZ=UTC

WORKDIR /app

# Install cron and timezone tools
RUN apt-get update && \
    apt-get install -y --no-install-recommends cron tzdata && \
    ln -snf /usr/share/zoneinfo/UTC /etc/localtime && \
    echo UTC > /etc/timezone && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy Python packages from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code and keys
COPY app/ app/
COPY scripts/ scripts/
COPY cron/ cron/
COPY student_private.pem .
COPY instructor_public.pem .

# Install cron job for the root user
RUN chmod 0644 cron/2fa-cron && \
    sed -i 's/\r//' cron/2fa-cron && \
    cat cron/2fa-cron | crontab -

# Create volume directories
RUN mkdir -p /data /cron && \
    chmod 755 /data /cron

EXPOSE 8080

CMD ["sh", "-c", "cron -L 8 && uvicorn app.main:app --host 0.0.0.0 --port 8080"]