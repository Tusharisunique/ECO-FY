from sqlalchemy import Column, String, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from core.database import Base
import uuid
from datetime import datetime

class Policy(Base):
    """Governance policies that require employee acknowledgement."""
    __tablename__ = "policies"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String, nullable=False)        # e.g. Ethics, Environment, HR
    document_url = Column(String, nullable=True)
    version = Column(String, default="1.0")
    is_active = Column(Boolean, default=True)
    effective_date = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    acknowledgements = relationship("PolicyAcknowledgement", back_populates="policy", cascade="all, delete-orphan")

class PolicyAcknowledgement(Base):
    """Records which employees have acknowledged a policy."""
    __tablename__ = "policy_acknowledgements"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    policy_id = Column(UUID(as_uuid=True), ForeignKey("policies.id", ondelete="CASCADE"), nullable=False)
    employee_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    acknowledged_at = Column(DateTime, default=datetime.utcnow)

    policy = relationship("Policy", back_populates="acknowledgements")

class Audit(Base):
    """Governance audits conducted on the organization or departments."""
    __tablename__ = "audits"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=True)
    title = Column(String, nullable=False)
    auditor = Column(String, nullable=True)
    status = Column(String, default="Scheduled")     # Scheduled, In Progress, Completed
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    findings = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    compliance_issues = relationship("ComplianceIssue", back_populates="audit", cascade="all, delete-orphan")

class ComplianceIssue(Base):
    """Issues identified during audits that require resolution."""
    __tablename__ = "compliance_issues"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    audit_id = Column(UUID(as_uuid=True), ForeignKey("audits.id", ondelete="CASCADE"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    severity = Column(String, default="Medium")     # Low, Medium, High, Critical
    status = Column(String, default="Open")          # Open, In Progress, Resolved
    due_date = Column(DateTime, nullable=True)
    resolved_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    audit = relationship("Audit", back_populates="compliance_issues")
