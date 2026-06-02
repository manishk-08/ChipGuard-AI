import uuid

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.models.bom import BOM, BOMItem, RiskScore

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/{bom_id}/risk-summary")
async def get_risk_summary(bom_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(BOM)
        .where(BOM.id == bom_id)
        .options(selectinload(BOM.items).selectinload(BOMItem.risk_score))
    )
    bom = result.scalar_one_or_none()
    if not bom:
        raise HTTPException(status_code=404, detail="BOM not found")

    high_risk = 0
    medium_risk = 0
    low_risk = 0
    compliance_flags = []

    for item in bom.items:
        score = item.risk_score
        if score:
            if score.total_score and score.total_score >= 70:
                high_risk += 1
            elif score.total_score and score.total_score >= 40:
                medium_risk += 1
            else:
                low_risk += 1
            if score.compliance_score and score.compliance_score >= 50:
                compliance_flags.append(f"Review compliance: {item.raw_part_number}")

    return {
        "bom_id": str(bom.id),
        "bom_name": bom.name,
        "total_items": len(bom.items),
        "high_risk_count": high_risk,
        "medium_risk_count": medium_risk,
        "low_risk_count": low_risk,
        "compliance_flags": compliance_flags,
        "disclaimer": "Decision-support only. Not legal advice. Consult a qualified trade compliance professional for final determinations.",
    }
