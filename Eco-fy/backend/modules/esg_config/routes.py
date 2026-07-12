from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from core.database import get_db
from core.dependencies import get_current_active_user
from .repository import EmissionFactorRepository, SustainabilityGoalRepository
from .schemas import (
    EmissionFactorCreate, EmissionFactorResponse,
    SustainabilityGoalCreate, SustainabilityGoalUpdate, SustainabilityGoalResponse
)

router = APIRouter()

# --- Emission Factors ---
@router.get("/emission-factors", response_model=list[EmissionFactorResponse])
def list_emission_factors(db: Session = Depends(get_db), _=Depends(get_current_active_user)):
    return EmissionFactorRepository(db).list_all()

@router.post("/emission-factors", response_model=EmissionFactorResponse, status_code=201)
def create_emission_factor(data: EmissionFactorCreate, db: Session = Depends(get_db), _=Depends(get_current_active_user)):
    return EmissionFactorRepository(db).create(data)

@router.delete("/emission-factors/{ef_id}", status_code=204)
def delete_emission_factor(ef_id: UUID, db: Session = Depends(get_db), _=Depends(get_current_active_user)):
    repo = EmissionFactorRepository(db)
    obj = repo.get_by_id(ef_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Emission factor not found")
    repo.delete(obj)

# --- Sustainability Goals ---
@router.get("/goals", response_model=list[SustainabilityGoalResponse])
def list_goals(organization_id: UUID, db: Session = Depends(get_db), _=Depends(get_current_active_user)):
    return SustainabilityGoalRepository(db).list_by_org(organization_id)

@router.post("/goals", response_model=SustainabilityGoalResponse, status_code=201)
def create_goal(data: SustainabilityGoalCreate, db: Session = Depends(get_db), _=Depends(get_current_active_user)):
    return SustainabilityGoalRepository(db).create(data)

@router.patch("/goals/{goal_id}", response_model=SustainabilityGoalResponse)
def update_goal(goal_id: UUID, data: SustainabilityGoalUpdate, db: Session = Depends(get_db), _=Depends(get_current_active_user)):
    repo = SustainabilityGoalRepository(db)
    goal = repo.get_by_id(goal_id)
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    return repo.update(goal, data)

@router.delete("/goals/{goal_id}", status_code=204)
def delete_goal(goal_id: UUID, db: Session = Depends(get_db), _=Depends(get_current_active_user)):
    repo = SustainabilityGoalRepository(db)
    goal = repo.get_by_id(goal_id)
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    repo.delete(goal)
