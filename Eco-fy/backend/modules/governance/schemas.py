from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional

class PolicyBase(BaseModel):
    organization_id: Optional[UUID] = None
    title: str
    description: Optional[str] = None
    category: str
    document_url: Optional[str] = None
    version: str = "1.0"
    is_active: bool = True
    effective_date: datetime

class PolicyCreate(PolicyBase):
    pass

class PolicyResponse(PolicyBase):
    id: UUID
    created_at: datetime
    model_config = {"from_attributes": True}

class AcknowledgementCreate(BaseModel):
    policy_id: UUID
    employee_id: UUID

class AcknowledgementResponse(AcknowledgementCreate):
    id: UUID
    acknowledged_at: datetime
    model_config = {"from_attributes": True}

class AuditBase(BaseModel):
    organization_id: Optional[UUID] = None
    title: str
    auditor: Optional[str] = None
    status: str = "Scheduled"
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    findings: Optional[str] = None

class AuditCreate(AuditBase):
    pass

class AuditUpdate(BaseModel):
    status: Optional[str] = None
    findings: Optional[str] = None
    end_date: Optional[datetime] = None

class AuditResponse(AuditBase):
    id: UUID
    created_at: datetime
    model_config = {"from_attributes": True}

class ComplianceIssueBase(BaseModel):
    audit_id: UUID
    title: str
    description: Optional[str] = None
    severity: str = "Medium"
    status: str = "Open"
    due_date: Optional[datetime] = None

class ComplianceIssueCreate(ComplianceIssueBase):
    pass

class ComplianceIssueUpdate(BaseModel):
    status: Optional[str] = None
    resolved_at: Optional[datetime] = None

class ComplianceIssueResponse(ComplianceIssueBase):
    id: UUID
    resolved_at: Optional[datetime] = None
    created_at: datetime
    model_config = {"from_attributes": True}
