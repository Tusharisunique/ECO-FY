from sqlalchemy import Column, String, DateTime, ForeignKey, Text, Integer, Boolean, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from core.database import Base
import uuid
from datetime import datetime

class Badge(Base):
    """Badges awarded to employees for achieving milestones."""
    __tablename__ = "badges"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    icon = Column(String, nullable=True)           # Icon name or URL
    category = Column(String, nullable=False)       # Environmental, Social, Governance
    xp_threshold = Column(Integer, default=0)       # Min XP to earn this badge
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    employee_badges = relationship("EmployeeBadge", back_populates="badge", cascade="all, delete-orphan")

class EmployeeBadge(Base):
    """Junction: which employees have earned which badges."""
    __tablename__ = "employee_badges"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    employee_id = Column(UUID(as_uuid=True), ForeignKey("employees.id", ondelete="CASCADE"), nullable=False)
    badge_id = Column(UUID(as_uuid=True), ForeignKey("badges.id", ondelete="CASCADE"), nullable=False)
    awarded_at = Column(DateTime, default=datetime.utcnow)

    employee = relationship("Employee", foreign_keys=[employee_id])
    badge = relationship("Badge", back_populates="employee_badges")

class Reward(Base):
    """Redeemable rewards for accumulated XP."""
    __tablename__ = "rewards"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    xp_cost = Column(Integer, nullable=False)
    quantity_available = Column(Integer, default=-1)  # -1 = unlimited
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Challenge(Base):
    """Time-bound challenges that encourage employees to complete ESG tasks."""
    __tablename__ = "challenges"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String, nullable=False)
    xp_reward = Column(Integer, default=100)
    target_value = Column(Float, nullable=True)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class XPTransaction(Base):
    """Audit log of all XP earned or spent by employees."""
    __tablename__ = "xp_transactions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    employee_id = Column(UUID(as_uuid=True), ForeignKey("employees.id", ondelete="CASCADE"), nullable=False)
    amount = Column(Integer, nullable=False)           # positive = earned, negative = spent
    reason = Column(String, nullable=False)            # e.g. "CSR Activity", "Badge Unlock"
    reference_id = Column(UUID(as_uuid=True), nullable=True)  # source record id
    created_at = Column(DateTime, default=datetime.utcnow)

    employee = relationship("Employee", foreign_keys=[employee_id])
