# Blueprint QA

AI-powered quality assurance for construction and engineering drawings. Upload a PDF and Claude claude-opus-4-6 will flag missing tags, dimension mismatches, unlabeled elements, and more.

## Live Demo

| Service | URL |
|---|---|
| Frontend | https://blueprint-qa-git-main-shlok-thakkars-projects.vercel.app |
| Backend API | https://blueprint-qa-3.onrender.com |
| API docs (Swagger) | https://blueprint-qa-3.onrender.com/docs |

## Deployment

- **Single URL (simplest):** deploy the Docker image from [`backend/Dockerfile`](backend/Dockerfile) on Render, [Fly.io](https://fly.io) ([`fly.toml`](fly.toml)), or Railway. The container serves the API and the static SPA; the UI uses same-origin `/api/...` (`.env.production` is excluded from the Docker build via [`.dockerignore`](.dockerignore)).
- **Split frontend + API:** point a Vercel project at the [`frontend/`](frontend/) directory. [`frontend/vercel.json`](frontend/vercel.json) treats the app as a static export (`index.html` + SPA rewrites). Keep [`frontend/.env.production`](frontend/.env.production) set to your public API origin.

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | SvelteKit + Tailwind CSS (deployed on Vercel) |
| Backend | FastAPI (Python 3.12, deployed on Render) |
| Database | PostgreSQL / Supabase (async SQLAlchemy + psycopg) |
| OCR | pytesseract + pdf2image |
| AI | Anthropic Claude claude-opus-4-6 (multimodal) |
| Storage | Local filesystem (/tmp on Render) |

---

## Quick Start — Docker Compose

### 1. Prerequisites
- Docker + Docker Compose
- An [Anthropic API key](https://console.anthropic.com/)

### 2. Configure environment

```bash
cp .env.example .env
# Edit .env and set your ANTHROPIC_API_KEY and DATABASE_URL
```

### 3. Start all services

```bash
docker-compose up --build
```

| Service | URL |
|---|---|
| Frontend | http://localhost:5173 |
| Backend API | http://localhost:8000 |
| API docs (Swagger) | http://localhost:8000/docs |

---

## Manual Dev Setup

### Backend

#### System requirements (macOS/Ubuntu)

```bash
# macOS
brew install poppler tesseract

# Ubuntu/Debian
sudo apt-get install poppler-utils tesseract-ocr tesseract-ocr-eng
```

#### Python setup

```bash
cd blueprint-qa
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
```

#### Configure and run

```bash
cp .env.example .env
# Fill in ANTHROPIC_API_KEY and DATABASE_URL

uvicorn backend.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
# Open http://localhost:5173
```

---

## Seed Demo Data

Insert 2 completed documents with 5 issues each (no real PDF files needed for viewing):

```bash
# From the project root with the venv active:
python -m backend.seed
```

---

## API Reference

| Method | Path | Description |
|---|---|---|
| POST | `/api/documents/upload` | Upload a PDF |
| GET | `/api/documents` | List all documents |
| GET | `/api/documents/{id}` | Get document details |
| DELETE | `/api/documents/{id}` | Delete document + issues |
| POST | `/api/analysis/{id}/run` | Run QA analysis |
| GET | `/api/analysis/{id}/issues` | Get issues for a document |
| GET | `/api/analysis/{id}/summary` | Issue summary stats |

Interactive docs: https://blueprint-qa-3.onrender.com/docs

---

## Project Structure

```
blueprint-qa/
├── backend/
│   ├── main.py               # FastAPI app + lifespan
│   ├── config.py             # Pydantic settings
│   ├── database.py           # Async SQLAlchemy engine
│   ├── models/               # SQLAlchemy ORM models
│   ├── schemas/              # Pydantic request/response schemas
│   ├── routers/              # API route handlers
│   ├── services/
│   │   ├── ocr_service.py    # pdf2image + pytesseract
│   │   ├── llm_service.py    # Claude claude-opus-4-6 multimodal calls
│   │   └── qa_service.py     # Pipeline orchestration
│   ├── storage/              # Local storage adapter
│   ├── seed.py               # Demo data seeder
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── routes/           # SvelteKit pages + server load functions
│   │   └── lib/
│   │       ├── api.ts        # Typed API client
│   │       ├── components/   # Svelte UI components
│   │       └── stores/       # Svelte writable stores
│   └── package.json
├── docker-compose.yml
├── render.yaml               # Render deployment config
├── .env.example
└── README.md
```

---

## Deployment

### Backend (Render)
- Runtime: Docker
- Dockerfile: `./backend/Dockerfile`
- Docker Build Context: `.` (repo root)
- Environment variables: `DATABASE_URL`, `ANTHROPIC_API_KEY`, `UPLOAD_DIR=/tmp/uploads`

### Frontend (Vercel)
- Framework: SvelteKit
- Root directory: `frontend`
- Connected to GitHub `shlok1806/blueprint-qa`

### Database (Supabase)
- PostgreSQL with SSL required
- Tables: `documents`, `issues`
