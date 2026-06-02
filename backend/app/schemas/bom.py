import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class BOMCreate(BaseModel):
    name: str


class BOMItemResponse(BaseModel):
    id: uuid.UUID
    raw_part_number: str
    normalized_mpn: Optional[str] = None
    manufacturer: Optional[str] = None
    quantity: Optional[int] = None
    description: Optional[str] = None
    matched_part_id: Optional[uuid.UUID] = None

    model_config = {"from_attributes": True}


class BOMResponse(BaseModel):
    id: uuid.UUID
    user_id: str
    name: str
    status: str
    total_risk_score: Optional[float] = None
    created_at: datetime
    updated_at: datetime
    items: list[BOMItemResponse] = []

    model_config = {"from_attributes": True}


class BOMListResponse(BaseModel):
    id: uuid.UUID
    name: str
    status: str
    total_risk_score: Optional[float] = None
    created_at: datetime

    model_config = {"from_attributes": True}


class RiskReportResponse(BaseModel):
    bom: BOMResponse
    summary: str
    high_risk_count: int
    medium_risk_count: int
    low_risk_count: int
    compliance_flags: list[str]
