# -------------------------------
# Base Image
# -------------------------------
FROM python:3.11-slim AS base

# -------------------------------
# Environment Settings
# -------------------------------
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# -------------------------------
# System Dependencies
# -------------------------------
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# -------------------------------
# Create Non-Root User
# -------------------------------
RUN useradd -m appuser

# -------------------------------
# Working Directory
# -------------------------------
WORKDIR /app

# -------------------------------
# Python Dependencies
# -------------------------------
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# -------------------------------
# Application Code
# -------------------------------
COPY app ./app

# -------------------------------
# Permissions
# -------------------------------
RUN chown -R appuser:appuser /app

USER appuser

# -------------------------------
# Expose Port
# -------------------------------
EXPOSE 8000

# -------------------------------
# Start Command
# -------------------------------
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
