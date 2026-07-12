from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from typing import Optional
from core.database import get_db
from core.dependencies import get_current_active_user
from .repository import PolicyRepository, AcknowledgementRepository, AuditRepository, ComplianceIssueRepository
from .schemas import (
    PolicyCreate, PolicyResponse,
    AcknowledgementCreate, AcknowledgementResponse,
    AuditCreate, AuditUpdate, AuditResponse,
    ComplianceIssueCreate, ComplianceIssueUpdate, ComplianceIssueResponse
)

router = APIRouter()

# --- Policies ---
@router.get("/policies", response_model=list[PolicyResponse])
def list_policies(organization_id: Optional[UUID] = None, db: Session = Depends(get_db), _=Depends(get_current_active_user)):
    if organization_id:
        return PolicyRepository(db).list_by_org(organization_id)
    from .models import Policy
    return db.query(Policy).all()

@router.post("/policies", response_model=PolicyResponse, status_code=201)
def create_policy(data: PolicyCreate, db: Session = Depends(get_db), _=Depends(get_current_active_user)):
    return PolicyRepository(db).create(data)

@router.delete("/policies/{policy_id}", status_code=204)
def delete_policy(policy_id: UUID, db: Session = Depends(get_db), _=Depends(get_current_active_user)):
    repo = PolicyRepository(db)
    p = repo.get_by_id(policy_id)
    if not p:
        raise HTTPException(status_code=404, detail="Policy not found")
    repo.delete(p)

# --- Acknowledgements ---
@router.post("/policy-acknowledgements", response_model=AcknowledgementResponse, status_code=201)
def acknowledge_policy(data: AcknowledgementCreate, db: Session = Depends(get_db), _=Depends(get_current_active_user)):
    return AcknowledgementRepository(db).acknowledge(data)

@router.get("/policy-acknowledgements/{policy_id}", response_model=list[AcknowledgementResponse])
def list_acknowledgements(policy_id: UUID, db: Session = Depends(get_db), _=Depends(get_current_active_user)):
    return AcknowledgementRepository(db).list_by_policy(policy_id)

# --- Audits ---
@router.get("/audits", response_model=list[AuditResponse])
def list_audits(organization_id: Optional[UUID] = None, db: Session = Depends(get_db), _=Depends(get_current_active_user)):
    if organization_id:
        return AuditRepository(db).list_by_org(organization_id)
    from .models import Audit
    return db.query(Audit).all()

@router.post("/audits", response_model=AuditResponse, status_code=201)
def create_audit(data: AuditCreate, db: Session = Depends(get_db), _=Depends(get_current_active_user)):
    return AuditRepository(db).create(data)

@router.patch("/audits/{audit_id}", response_model=AuditResponse)
def update_audit(audit_id: UUID, data: AuditUpdate, db: Session = Depends(get_db), _=Depends(get_current_active_user)):
    repo = AuditRepository(db)
    audit = repo.get_by_id(audit_id)
    if not audit:
        raise HTTPException(status_code=404, detail="Audit not found")
    return repo.update(audit, data)

# --- Compliance Issues ---
@router.get("/compliance-issues", response_model=list[ComplianceIssueResponse])
def list_issues(audit_id: Optional[UUID] = None, db: Session = Depends(get_db), _=Depends(get_current_active_user)):
    if audit_id:
        return ComplianceIssueRepository(db).list_by_audit(audit_id)
    from .models import ComplianceIssue
    return db.query(ComplianceIssue).all()

@router.post("/compliance-issues", response_model=ComplianceIssueResponse, status_code=201)
def create_issue(data: ComplianceIssueCreate, db: Session = Depends(get_db), _=Depends(get_current_active_user)):
    return ComplianceIssueRepository(db).create(data)

@router.patch("/compliance-issues/{issue_id}", response_model=ComplianceIssueResponse)
def update_issue(issue_id: UUID, data: ComplianceIssueUpdate, db: Session = Depends(get_db), _=Depends(get_current_active_user)):
    repo = ComplianceIssueRepository(db)
    issue = repo.get_by_id(issue_id)
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")
    return repo.update(issue, data)
