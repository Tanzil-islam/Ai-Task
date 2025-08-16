# Builder stage to compile dependencies
FROM python:3.11-slim AS builder

# Install build tools for C and Rust compilation
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    cargo \
    rustc \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Upgrade pip and build wheels
RUN pip install --upgrade pip \
    && pip wheel --no-deps -r requirements.txt -w wheels

# Final stage
FROM python:3.11-slim

WORKDIR /app

# Copy prebuilt wheels and application code
COPY --from=builder /app/wheels /wheels
COPY requirements.txt .
COPY app.py .
COPY models.py .
COPY utils.py .

# Install prebuilt wheels
RUN pip install --no-index --find-links=/wheels -r requirements.txt

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
