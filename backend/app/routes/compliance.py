from fastapi import APIRouter, HTTPException

from app.services.compliance import ComplianceScreener

router = APIRouter(prefix="/compliance", tags=["compliance"])


@router.post("/screen")
async def screen_entity(name: str):
    screener = ComplianceScreener()
    results = screener.screen_name(name)
    return {
        "entity_name": name,
        "matches": results,
        "disclaimer": "Decision-support only. Not legal advice. Consult a qualified trade compliance professional for final determinations.",
    }


@router.get("/lists")
async def get_available_lists():
    return {
        "lists": [
            "BIS Entity List",
            "OFAC Sanctions List",
            "Denied Persons List",
            "Unverified List",
        ],
        "last_updated": "2026-01-01",
        "total_entities": 0,
    }
