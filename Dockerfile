
FROM python:3.13-slim AS builder

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    cargo \
    rustc \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip \
    && pip wheel --no-deps -r requirements.txt -w wheels

# Final stage
FROM python:3.13-slim

WORKDIR /app

COPY --from=builder /app/wheels /wheels
COPY requirements.txt .
COPY app/ ./app/  # Copy the entire app directory

RUN pip install --no-index --find-links=/wheels -r requirements.txt

EXPOSE 8000

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port $PORT"]s

