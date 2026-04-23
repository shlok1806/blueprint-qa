# ── Stage 1: Build the SvelteKit static frontend ─────────────────────────────
FROM node:20-bookworm-slim AS frontend-builder
WORKDIR /app
COPY frontend/package*.json ./
ENV NODE_OPTIONS=--max-old-space-size=6144
RUN npm ci --no-audit --no-fund
COPY frontend/ ./
RUN npm run build

# ── Stage 2: Python backend + static frontend ────────────────────────────────
FROM python:3.12-slim-bookworm

RUN apt-get update && apt-get install -y \
    poppler-utils \
    tesseract-ocr \
    tesseract-ocr-eng \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY backend/ ./backend/
COPY --from=frontend-builder /app/build ./backend/static/

EXPOSE 8000

CMD ["sh", "-c", "exec uvicorn backend.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
