import uuid

from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.models.bom import BOM, BOMItem
from app.schemas.bom import BOMListResponse, BOMResponse
from app.services.bom_parser import BOMParser

router = APIRouter(prefix="/boms", tags=["boms"])


@router.post("/upload", response_model=BOMResponse)
async def upload_bom(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
):
    if not file.filename or not (file.filename.endswith(".csv") or file.filename.endswith(".xlsx")):
        raise HTTPException(status_code=400, detail="Only CSV and XLSX files are supported")

    content = await file.read()
    parser = BOMParser()
    try:
        items = parser.parse(content, file.filename)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    bom = BOM(user_id="anonymous", name=file.filename or "untitled", status="pending")
    db.add(bom)
    await db.flush()

    for item in items:
        bom_item = BOMItem(
            bom_id=bom.id,
            raw_part_number=item["raw_part_number"],
            manufacturer=item.get("manufacturer"),
            quantity=item.get("quantity"),
            description=item.get("description"),
        )
        db.add(bom_item)

    await db.commit()
    await db.refresh(bom, ["items"])
    return bom


@router.get("/", response_model=list[BOMListResponse])
async def list_boms(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(BOM).options(selectinload(BOM.items)).order_by(BOM.created_at.desc())
    )
    return result.scalars().all()


@router.get("/{bom_id}", response_model=BOMResponse)
async def get_bom(bom_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(BOM).where(BOM.id == bom_id).options(selectinload(BOM.items))
    )
    bom = result.scalar_one_or_none()
    if not bom:
        raise HTTPException(status_code=404, detail="BOM not found")
    return bom


@router.delete("/{bom_id}", status_code=204)
async def delete_bom(bom_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(BOM).where(BOM.id == bom_id))
    bom = result.scalar_one_or_none()
    if not bom:
        raise HTTPException(status_code=404, detail="BOM not found")
    await db.delete(bom)
    await db.commit()
