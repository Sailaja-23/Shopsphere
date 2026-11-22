
FROM python:3.12-slim

# Python runtime optimizations
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies separately for better build caching
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Create a non-root application user
RUN addgroup --system app && \
    adduser --system --ingroup app app

# Copy application files with correct ownership
COPY --chown=app:app . .

# Run application as non-root user
USER app

EXPOSE 8000

# Container health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/docs')" || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
