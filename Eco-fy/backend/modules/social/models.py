from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Text, Boolean, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from core.database import Base
import uuid
from datetime import datetime

class CSRActivity(Base):
    """Corporate Social Responsibility activities available for employee participation."""
    __tablename__ = "csr_activities"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String, nullable=False)  # e.g. Volunteering, Donation, Awareness
    xp_reward = Column(Integer, default=50)
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    participations = relationship("EmployeeParticipation", back_populates="csr_activity", cascade="all, delete-orphan")

class EmployeeParticipation(Base):
    """Records an employee's participation in a CSR activity, including evidence and approval state."""
    __tablename__ = "employee_participations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    csr_activity_id = Column(UUID(as_uuid=True), ForeignKey("csr_activities.id", ondelete="CASCADE"), nullable=False)
    employee_id = Column(UUID(as_uuid=True), ForeignKey("employees.id", ondelete="CASCADE"), nullable=False)
    hours_contributed = Column(Float, default=0.0)
    notes = Column(Text, nullable=True)
    status = Column(String, default="Pending")  # Pending, Approved, Rejected
    evidence_url = Column(String, nullable=True)
    reviewed_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    reviewed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    csr_activity = relationship("CSRActivity", back_populates="participations")
    employee = relationship("Employee", foreign_keys=[employee_id])
