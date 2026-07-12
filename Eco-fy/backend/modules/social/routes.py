from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from typing import Optional
from core.database import get_db
from core.dependencies import get_current_active_user
from .repository import CSRActivityRepository, ParticipationRepository
from .schemas import (
    CSRActivityCreate, CSRActivityResponse,
    ParticipationCreate, ParticipationReview, ParticipationResponse
)

router = APIRouter()

# --- CSR Activities ---
@router.get("/activities", response_model=list[CSRActivityResponse])
def list_activities(organization_id: Optional[UUID] = None, db: Session = Depends(get_db), _=Depends(get_current_active_user)):
    if organization_id:
        return CSRActivityRepository(db).list_by_org(organization_id)
    from .models import CSRActivity
    return db.query(CSRActivity).all()

@router.post("/activities", response_model=CSRActivityResponse, status_code=201)
def create_activity(data: CSRActivityCreate, db: Session = Depends(get_db), _=Depends(get_current_active_user)):
    return CSRActivityRepository(db).create(data)

@router.get("/activities/{activity_id}", response_model=CSRActivityResponse)
def get_activity(activity_id: UUID, db: Session = Depends(get_db), _=Depends(get_current_active_user)):
    activity = CSRActivityRepository(db).get_by_id(activity_id)
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    return activity

@router.delete("/activities/{activity_id}", status_code=204)
def delete_activity(activity_id: UUID, db: Session = Depends(get_db), _=Depends(get_current_active_user)):
    repo = CSRActivityRepository(db)
    obj = repo.get_by_id(activity_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Activity not found")
    repo.delete(obj)

# --- Participation & Approval Workflow ---
@router.post("/participations", response_model=ParticipationResponse, status_code=201)
def log_participation(data: ParticipationCreate, db: Session = Depends(get_db), _=Depends(get_current_active_user)):
    return ParticipationRepository(db).create(data)

@router.get("/participations/pending", response_model=list[ParticipationResponse])
def list_pending(organization_id: Optional[UUID] = None, db: Session = Depends(get_db), _=Depends(get_current_active_user)):
    repo = ParticipationRepository(db)
    if organization_id:
        return repo.list_pending(organization_id)
    from .models import EmployeeParticipation
    return db.query(EmployeeParticipation).filter(EmployeeParticipation.status == "Pending").all()

@router.patch("/participations/{participation_id}/review", response_model=ParticipationResponse)
def review_participation(
    participation_id: UUID, review: ParticipationReview,
    db: Session = Depends(get_db), _=Depends(get_current_active_user)
):
    repo = ParticipationRepository(db)
    p = repo.get_by_id(participation_id)
    if not p:
        raise HTTPException(status_code=404, detail="Participation not found")
    if review.status not in ("Approved", "Rejected"):
        raise HTTPException(status_code=400, detail="Status must be Approved or Rejected")
    was_pending = p.status == "Pending"
    updated_p = repo.review(p, review)
    
    if was_pending and updated_p.status == "Approved":
        from modules.gamification.repository import XPRepository
        from modules.gamification.schemas import XPTransactionCreate
        
        activity = updated_p.csr_activity
        if activity and activity.xp_reward:
            xp_repo = XPRepository(db)
            xp_repo.award(XPTransactionCreate(
                employee_id=updated_p.employee_id,
                amount=activity.xp_reward,
                reason=f"Completed CSR Activity: {activity.title}"
            ))

    return updated_p
