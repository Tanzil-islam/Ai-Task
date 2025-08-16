# Use official Python slim image for smaller footprint
FROM python:3.11-slim AS builder

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install build dependencies and compile wheels
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    cargo \
    rustc \
    && pip install --no-cache-dir --upgrade pip \
    && pip wheel --no-deps -r requirements.txt -w wheels

# Final stage
FROM python:3.11-slim

WORKDIR /app

# Copy prebuilt wheels
COPY --from=builder /app/wheels /wheels
COPY requirements.txt .
COPY app.py .
COPY models.py .
COPY utils.py .

# Install wheels
RUN pip install --no-index --find-links=/wheels -r requirements.txt

# Expose port 8000
EXPOSE 8000

# Command to run FastAPI with Uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]