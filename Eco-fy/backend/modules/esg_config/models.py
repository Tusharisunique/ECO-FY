from sqlalchemy import Column, String, Float, DateTime, Boolean, ForeignKey, Enum as PGEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from core.database import Base
import uuid
import enum
from datetime import datetime

class ESGCategory(str, enum.Enum):
    ENVIRONMENTAL = "Environmental"
    SOCIAL = "Social"
    GOVERNANCE = "Governance"

class GoalStatus(str, enum.Enum):
    ACTIVE = "Active"
    COMPLETED = "Completed"
    PAUSED = "Paused"

class EmissionFactor(Base):
    """Reference table for greenhouse gas emission conversion factors."""
    __tablename__ = "emission_factors"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False, unique=True)
    category = Column(String, nullable=False)           # e.g. Travel, Energy, Fuel
    unit = Column(String, nullable=False)               # e.g. km, kWh, litre
    co2e_per_unit = Column(Float, nullable=False)       # kg CO2e per unit
    source = Column(String, nullable=True)              # e.g. IPCC 2023, DEFRA
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class SustainabilityGoal(Base):
    """Org-level sustainability targets (e.g. Net-Zero by 2030)."""
    __tablename__ = "sustainability_goals"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id", ondelete="CASCADE"))
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    category = Column(String, nullable=False)
    target_value = Column(Float, nullable=False)
    current_value = Column(Float, default=0.0)
    unit = Column(String, nullable=False)
    target_date = Column(DateTime, nullable=False)
    status = Column(String, default=GoalStatus.ACTIVE)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
