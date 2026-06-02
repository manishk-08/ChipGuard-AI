import uuid
from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class BOM(TimestampMixin, Base):
    __tablename__ = "boms"

    user_id: Mapped[str] = mapped_column(String, index=True)
    name: Mapped[str] = mapped_column(String)
    status: Mapped[str] = mapped_column(String, default="pending")
    total_risk_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    file_path: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    items: Mapped[list["BOMItem"]] = relationship(back_populates="bom", cascade="all, delete-orphan")


class BOMItem(TimestampMixin, Base):
    __tablename__ = "bom_items"

    bom_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("boms.id", ondelete="CASCADE"))
    raw_part_number: Mapped[str] = mapped_column(String)
    normalized_mpn: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    manufacturer: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    quantity: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    matched_part_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("parts.id"), nullable=True)

    bom: Mapped["BOM"] = relationship(back_populates="items")
    matched_part: Mapped[Optional["Part"]] = relationship()
    risk_score: Mapped[Optional["RiskScore"]] = relationship(back_populates="bom_item", uselist=False)


class Part(TimestampMixin, Base):
    __tablename__ = "parts"

    mpn: Mapped[str] = mapped_column(String, index=True, unique=True)
    manufacturer: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    category: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    lifecycle_status: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    possible_eccn: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    hs_code: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    datasheet_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    offers: Mapped[list["SupplierOffer"]] = relationship(back_populates="part", cascade="all, delete-orphan")


class SupplierOffer(TimestampMixin, Base):
    __tablename__ = "supplier_offers"

    part_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("parts.id", ondelete="CASCADE"))
    distributor: Mapped[str] = mapped_column(String)
    stock: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    price: Mapped[Optional[Decimal]] = mapped_column(Float, nullable=True)
    lead_time_days: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    is_authorized: Mapped[bool] = mapped_column(Boolean, default=True)
    country: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    offer_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    last_checked_at: Mapped[datetime] = mapped_column(DateTime)

    part: Mapped["Part"] = relationship(back_populates="offers")


class RiskScore(TimestampMixin, Base):
    __tablename__ = "risk_scores"

    bom_item_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("bom_items.id", ondelete="CASCADE"), unique=True
    )
    availability_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    lifecycle_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    supplier_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    lead_time_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    compliance_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    total_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    explanation: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    bom_item: Mapped["BOMItem"] = relationship(back_populates="risk_score")


class RestrictedEntity(TimestampMixin, Base):
    __tablename__ = "restricted_entities"

    name: Mapped[str] = mapped_column(String, index=True)
    list_source: Mapped[str] = mapped_column(String)
    country: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    restriction_type: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    reference_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)


class ScreeningResult(TimestampMixin, Base):
    __tablename__ = "screening_results"

    bom_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("boms.id", ondelete="CASCADE"))
    entity_name: Mapped[str] = mapped_column(String)
    match_score: Mapped[float] = mapped_column(Float)
    list_source: Mapped[str] = mapped_column(String)
    decision_status: Mapped[str] = mapped_column(String, default="review_required")
    reviewed_by: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
