# ChipGuard AI

BOM risk and compliance intelligence for electronics teams.

## Stack

| Layer | Choice |
|---|---|
| Backend | FastAPI + SQLAlchemy 2.0 (async) + Celery + Redis |
| Frontend | Next.js + Tailwind CSS + Recharts |
| Database | PostgreSQL with row-level security |
| Auth | Supabase Auth |
| PDF | WeasyPrint (server-side) |
| Model | `opencode/big-pickle` (free) |

## Project Structure

```
chipguard-ai/
  backend/              # FastAPI application
    app/
      models/           # SQLAlchemy ORM models
      routes/           # API endpoint handlers
      services/         # Business logic
        bom_parser.py   # CSV/XLSX BOM ingestion
        risk_engine.py  # Risk scoring formulas
        compliance.py   # Entity/sanctions screening
        sourcing.py     # Octopart/Nexar integration
      tasks/            # Celery async workers
      schemas/          # Pydantic request/response models
    tests/
    alembic/            # DB migrations
    requirements.txt
  frontend/             # Next.js application
    app/                # App router pages
    components/         # Shared UI components
    lib/                # API client, utils
    package.json
  data/                 # Compliance list seeds (git-tracked CSVs)
  docs/
  AGENTS.md
```

## Dev Commands (Windows PowerShell)

### Backend
```powershell
cd backend
python -m venv .venv; .\.venv\Scripts\Activate
pip install -r requirements.txt
# Start API
uvicorn app.main:app --reload --port 8000
# Start Celery worker (separate terminal)
celery -A app.tasks worker --loglevel=info --pool=solo
# Run tests
pytest -v
```

### Frontend
```powershell
cd frontend
npm install
npm run dev        # starts on :3000
npm test
npm run lint
```

### Database
```powershell
# Apply migrations
cd backend
alembic upgrade head
# Create new migration
alembic revision --autogenerate -m "description"
```

## Security & Compliance Constraints (MANDATORY)

- **Never** output "legally compliant", "approved for export", or any legal conclusion. Use only: `"Review required"`, `"Flag for compliance review"`, `"Decision-support only"`.
- All distributor API calls (Octopart, DigiKey, etc.) must be **server-side only**. Never expose API keys to the frontend.
- PostgreSQL **row-level security**: User A's BOMs must be invisible to User B.
- BOM files uploaded must be encrypted at rest.
- Add compliance disclaimer to every generated report.
- No secrets in code — use `.env` files for all API keys.
- Rate-limit BOM upload endpoints (prevent abuse/leakage).

## Risk Scoring Formula

```
Total = Availability(0.35) + Lifecycle(0.20) + SupplierConcentration(0.20)
        + LeadTime(0.15) + ComplianceReview(0.10)
```

Each sub-score is 0-100. Total is 0-100. Higher = riskier.

## Data Sources

| Data | Source | Access |
|---|---|---|
| Component availability/price | Octopart/Nexar GraphQL API | Free tier, API key |
| Lifecycle status | Octopart API + manufacturer sites | Via Octopart |
| Restricted parties | BIS Entity List, OFAC sanctions | Public CSVs |
| Distributor stock | DigiKey, Mouser, Arrow APIs | Free/registration |

## Phase Plan (6-Month MVP)

1. **Month 1** — Backend scaffold + BOM CSV/XLSX parser + DB models
2. **Month 2** — Octopart integration + risk scoring engine
3. **Month 3** — Frontend dashboard + PDF report generation
4. **Month 4** — Compliance screening module (Entity List, sanctions)
5. **Month 5** — User testing, feedback, iteration
6. **Month 6** — Polish, deploy (Railway + Vercel), YC app prep

## Model Setup

```jsonc
// opencode.json
{
  "$schema": "https://opencode.ai/config.json",
  "model": "opencode/big-pickle"
}
```

Run `/connect` in opencode → select OpenCode Zen → paste API key from https://opencode.ai/auth

## OpenCode Workflow for This Project

1. Always read AGENTS.md first
2. Backend changes: write model → write schema → write service → write route → write test
3. Frontend changes: write component → write story/page → verify against API
4. Run `pytest` for backend, `npm test` for frontend before finishing
5. Security review: any compliance-related change needs double-check on disclaimer language
