from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from core.database import get_db
from core.dependencies import get_current_active_user
from .repository import BadgeRepository, RewardRepository, ChallengeRepository, XPRepository
from .schemas import (
    BadgeCreate, BadgeResponse, EmployeeBadgeResponse,
    RewardCreate, RewardResponse,
    ChallengeCreate, ChallengeResponse,
    XPTransactionCreate, XPTransactionResponse,
    LeaderboardEntry
)

router = APIRouter()

# --- Badges ---
@router.get("/badges", response_model=list[BadgeResponse])
def list_badges(organization_id: UUID, db: Session = Depends(get_db), _=Depends(get_current_active_user)):
    return BadgeRepository(db).list_by_org(organization_id)

@router.post("/badges", response_model=BadgeResponse, status_code=201)
def create_badge(data: BadgeCreate, db: Session = Depends(get_db), _=Depends(get_current_active_user)):
    return BadgeRepository(db).create(data)

@router.post("/badges/{badge_id}/award/{employee_id}", response_model=EmployeeBadgeResponse, status_code=201)
def award_badge(badge_id: UUID, employee_id: UUID, db: Session = Depends(get_db), _=Depends(get_current_active_user)):
    repo = BadgeRepository(db)
    badge = repo.get_by_id(badge_id)
    if not badge:
        raise HTTPException(status_code=404, detail="Badge not found")
    return repo.award_to_employee(employee_id, badge_id)

@router.get("/employees/{employee_id}/badges", response_model=list[EmployeeBadgeResponse])
def list_employee_badges(employee_id: UUID, db: Session = Depends(get_db), _=Depends(get_current_active_user)):
    return BadgeRepository(db).list_employee_badges(employee_id)

# --- Rewards ---
@router.get("/rewards", response_model=list[RewardResponse])
def list_rewards(organization_id: UUID, db: Session = Depends(get_db), _=Depends(get_current_active_user)):
    return RewardRepository(db).list_by_org(organization_id)

@router.post("/rewards", response_model=RewardResponse, status_code=201)
def create_reward(data: RewardCreate, db: Session = Depends(get_db), _=Depends(get_current_active_user)):
    return RewardRepository(db).create(data)

# --- Challenges ---
@router.get("/challenges", response_model=list[ChallengeResponse])
def list_challenges(organization_id: UUID, db: Session = Depends(get_db), _=Depends(get_current_active_user)):
    return ChallengeRepository(db).list_by_org(organization_id)

@router.post("/challenges", response_model=ChallengeResponse, status_code=201)
def create_challenge(data: ChallengeCreate, db: Session = Depends(get_db), _=Depends(get_current_active_user)):
    return ChallengeRepository(db).create(data)

# --- XP ---
@router.post("/xp/award", response_model=XPTransactionResponse, status_code=201)
def award_xp(data: XPTransactionCreate, db: Session = Depends(get_db), _=Depends(get_current_active_user)):
    return XPRepository(db).award(data)

@router.get("/xp/{employee_id}/total")
def get_total_xp(employee_id: UUID, db: Session = Depends(get_db), _=Depends(get_current_active_user)):
    total = XPRepository(db).get_employee_total_xp(employee_id)
    return {"employee_id": str(employee_id), "total_xp": total}

# --- Leaderboard ---
@router.get("/leaderboard", response_model=list[LeaderboardEntry])
def get_leaderboard(organization_id: UUID, limit: int = 10, db: Session = Depends(get_db), _=Depends(get_current_active_user)):
    return XPRepository(db).get_leaderboard(organization_id, limit)
