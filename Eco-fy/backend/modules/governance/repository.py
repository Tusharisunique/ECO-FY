from sqlalchemy.orm import Session
from uuid import UUID
from datetime import datetime
from .models import Policy, PolicyAcknowledgement, Audit, ComplianceIssue
from .schemas import PolicyCreate, AcknowledgementCreate, AuditCreate, AuditUpdate, ComplianceIssueCreate, ComplianceIssueUpdate

class PolicyRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_by_org(self, organization_id: UUID):
        return self.db.query(Policy).filter(Policy.organization_id == organization_id).all()

    def get_by_id(self, policy_id: UUID):
        return self.db.query(Policy).filter(Policy.id == policy_id).first()

    def create(self, data: PolicyCreate):
        obj = Policy(**data.model_dump())
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete(self, obj: Policy):
        self.db.delete(obj)
        self.db.commit()

class AcknowledgementRepository:
    def __init__(self, db: Session):
        self.db = db

    def acknowledge(self, data: AcknowledgementCreate):
        obj = PolicyAcknowledgement(**data.model_dump())
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def list_by_policy(self, policy_id: UUID):
        return self.db.query(PolicyAcknowledgement).filter(PolicyAcknowledgement.policy_id == policy_id).all()

class AuditRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_by_org(self, organization_id: UUID):
        return self.db.query(Audit).filter(Audit.organization_id == organization_id).all()

    def get_by_id(self, audit_id: UUID):
        return self.db.query(Audit).filter(Audit.id == audit_id).first()

    def create(self, data: AuditCreate):
        obj = Audit(**data.model_dump())
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def update(self, audit: Audit, data: AuditUpdate):
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(audit, field, value)
        self.db.commit()
        self.db.refresh(audit)
        return audit

class ComplianceIssueRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_by_audit(self, audit_id: UUID):
        return self.db.query(ComplianceIssue).filter(ComplianceIssue.audit_id == audit_id).all()

    def get_by_id(self, issue_id: UUID):
        return self.db.query(ComplianceIssue).filter(ComplianceIssue.id == issue_id).first()

    def create(self, data: ComplianceIssueCreate):
        obj = ComplianceIssue(**data.model_dump())
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def update(self, issue: ComplianceIssue, data: ComplianceIssueUpdate):
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(issue, field, value)
        self.db.commit()
        self.db.refresh(issue)
        return issue
