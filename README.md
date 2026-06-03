# ChipGuard AI

**BOM Risk and Compliance Intelligence for Electronics Teams**

ChipGuard AI is a full-stack platform that ingests Bill of Materials (BOM) files, enriches component data via the Nexar/Octopart API, calculates supply-chain risk scores, and screens against global restricted-party lists — all within a modern async Python backend and a responsive Next.js dashboard.

---

## Architecture

```
chipguard-ai/
├── backend/                  # FastAPI application
│   ├── app/
│   │   ├── models/           # SQLAlchemy ORM models (BOM, Part, RiskScore, …)
│   │   ├── routes/           # REST endpoints (boms, compliance, reports)
│   │   ├── schemas/          # Pydantic request/response models
│   │   ├── services/         # Business logic layer
│   │   ├── tasks/            # Celery async workers
│   │   ├── config.py         # Environment-driven settings
│   │   ├── database.py       # Async engine & session factory
│   │   └── main.py           # FastAPI app entry point
│   ├── alembic/              # Database migrations
│   ├── tests/                # Pytest test suite
│   └── requirements.txt
├── frontend/                 # Next.js 15 application
│   ├── app/                  # App router pages & layouts
│   ├── components/           # Shared UI components
│   ├── lib/                  # API client utilities
│   └── package.json
└── data/                     # Compliance screening list seeds (CSV)
```

### Tech Stack

| Layer | Technology |
|---|---|
| API Framework | FastAPI (async) |
| ORM | SQLAlchemy 2.0 (async) |
| Database | PostgreSQL (asyncpg) / SQLite (dev) |
| Migrations | Alembic |
| Task Queue | Celery + Redis |
| Auth | JWT (python-jose) / Supabase Auth |
| Frontend | Next.js 15, React 19, Tailwind CSS 4 |
| Charts | Recharts |
| PDF Reports | WeasyPrint |
| Part Data | Nexar / Octopart GraphQL API |
| Compliance | BIS Entity List, OFAC Sanctions, Denied Persons List, Unverified List |

---

## Features

### BOM Ingestion
- Upload CSV or XLSX files via the dashboard or REST API
- Automatic column detection with alias support (e.g., `MPN`, `Part Number`, `Mfr`, `Qty`)
- Normalizes part numbers, quantities, and manufacturer names

### Risk Scoring
Multi-factor weighted scoring formula:

```
Total Risk = Availability (0.35)
           + Lifecycle (0.20)
           + Supplier Concentration (0.20)
           + Lead Time (0.15)
           + Compliance Review (0.10)
```

Each sub-score ranges 0–100; total ranges 0–100 (higher = riskier). Severity thresholds: **Low** (< 40), **Medium** (40–69), **High** (≥ 70).

### Part Enrichment
- Queries Nexar/Octopart GraphQL API for live pricing, stock levels, lifecycle status, and datasheet URLs
- Falls back to sensible defaults when API data is unavailable

### Compliance Screening
- Fuzzy name matching (token-sort ratio) against consolidated restricted-party lists
- Supports BIS Entity List, OFAC Sanctions, Denied Persons List, Unverified List
- All results include the disclaimer: *"Decision-support only. Not legal advice."*

### Async Task Processing
- Celery workers handle long-running BOM enrichment and compliance screening
- Configurable queues for `bom_processing` and `compliance` workloads

---

## Quick Start

### Prerequisites

- Python 3.12+
- Node.js 20+
- PostgreSQL (or SQLite for development)
- Redis (required for Celery)

### Backend Setup

```bash
cd backend
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\Activate
pip install -r requirements.txt

# Copy environment template
cp .env.example .env

# Start the API server
uvicorn app.main:app --reload --port 8000

# In a separate terminal, start the Celery worker
celery -A app.tasks.worker worker --loglevel=info --pool=solo
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev        # → http://localhost:3000
```

### Database Migrations

```bash
cd backend
alembic upgrade head
alembic revision --autogenerate -m "description"
```

---

## API Endpoints

| Method | Path | Description |
|---|---|---|
| `GET` | `/health` | Health check |
| `POST` | `/boms/upload` | Upload a BOM file (CSV/XLSX) |
| `GET` | `/boms/` | List all BOMs |
| `GET` | `/boms/{id}` | Get BOM details with items |
| `DELETE` | `/boms/{id}` | Delete a BOM |
| `GET` | `/reports/{bom_id}/risk-summary` | Aggregated risk report |
| `POST` | `/compliance/screen` | Screen entity name against restricted lists |
| `GET` | `/compliance/lists` | Available compliance lists |

---

## Environment Variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `DATABASE_URL` | Yes | `postgresql+asyncpg://…` | PostgreSQL connection string |
| `CORS_ORIGINS` | No | `http://localhost:3000` | Comma-separated allowed origins |
| `JWT_SECRET` | Yes | `change-me-in-production` | Signing key for JWT tokens |
| `REDIS_URL` | No | `redis://localhost:6379/0` | Celery broker & result backend |
| `OCTOPART_API_KEY` | No | — | Nexar client ID for part data |
| `SUPABASE_URL` | No | — | Supabase project URL |
| `SUPABASE_KEY` | No | — | Supabase anon key |
| `ENVIRONMENT` | No | `development` | Toggles debug logging, etc. |
| `NEXT_PUBLIC_API_URL` | Frontend | `http://localhost:8000` | Backend URL for Next.js rewrites |

---

## Deployment

### Backend (Render)

1. Connect your GitHub repository to Render.
2. Create a **Web Service** with:
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app.main:app --config gunicorn_conf.py`
3. Set the required environment variables (`DATABASE_URL`, `JWT_SECRET`, `CORS_ORIGINS`).
4. Optionally create a **Cron Job** or **Background Worker** for Celery tasks.

### Frontend (Vercel)

1. Import your GitHub repository.
2. Set **Root Directory** to `frontend`.
3. Vercel auto-detects Next.js — no additional framework configuration needed.
4. Set `NEXT_PUBLIC_API_URL` to your deployed backend URL.

---

## Testing

```bash
# Backend
cd backend
pytest -v

# Frontend
cd frontend
npm test
```

---

## Compliance Notice

ChipGuard AI is a **decision-support tool only**. It does not provide legal advice, export classification, or regulatory approval. All screening results and risk reports must be reviewed by a qualified trade compliance professional before making any business or shipping decisions.

---

## License

MIT
