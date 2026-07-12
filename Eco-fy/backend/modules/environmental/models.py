from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from core.database import Base
import uuid
from datetime import datetime

class CarbonTransaction(Base):
    """Records individual carbon-emitting activities logged by employees."""
    __tablename__ = "carbon_transactions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    employee_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=True)
    emission_factor_id = Column(UUID(as_uuid=True), ForeignKey("emission_factors.id"), nullable=True)
    
    activity_type = Column(String, nullable=False)       # e.g. "Business Travel", "Office Energy"
    description = Column(Text, nullable=True)
    quantity = Column(Float, nullable=False)             # raw quantity (km, kWh, etc.)
    unit = Column(String, nullable=False)
    co2e_kg = Column(Float, nullable=False)              # calculated CO2 equivalent in kg
    activity_date = Column(DateTime, nullable=False)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    employee = relationship("User", foreign_keys=[employee_id])
    emission_factor = relationship("EmissionFactor", foreign_keys=[emission_factor_id])
