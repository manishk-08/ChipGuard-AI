from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.config import settings
from app.database import engine
from app.models import Base
from app.routes import boms, compliance, reports


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables on startup (useful for SQLite dev; prod uses Alembic)
    if settings.database_url.startswith("sqlite"):
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(
    title="ChipGuard AI",
    description="BOM risk and compliance intelligence for electronics teams",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(boms.router)
app.include_router(compliance.router)
app.include_router(reports.router)


@app.get("/health")
async def health():
    return {"status": "ok", "version": "0.1.0"}
