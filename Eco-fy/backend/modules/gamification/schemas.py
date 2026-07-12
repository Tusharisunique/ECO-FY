from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional

class BadgeBase(BaseModel):
    organization_id: UUID
    name: str
    description: Optional[str] = None
    icon: Optional[str] = None
    category: str
    xp_threshold: int = 0
    is_active: bool = True

class BadgeCreate(BadgeBase):
    pass

class BadgeResponse(BadgeBase):
    id: UUID
    created_at: datetime
    model_config = {"from_attributes": True}

class EmployeeBadgeResponse(BaseModel):
    id: UUID
    employee_id: UUID
    badge_id: UUID
    awarded_at: datetime
    model_config = {"from_attributes": True}

class RewardBase(BaseModel):
    organization_id: UUID
    name: str
    description: Optional[str] = None
    xp_cost: int
    quantity_available: int = -1
    is_active: bool = True

class RewardCreate(RewardBase):
    pass

class RewardResponse(RewardBase):
    id: UUID
    created_at: datetime
    model_config = {"from_attributes": True}

class ChallengeBase(BaseModel):
    organization_id: UUID
    title: str
    description: Optional[str] = None
    category: str
    xp_reward: int = 100
    target_value: Optional[float] = None
    start_date: datetime
    end_date: datetime
    is_active: bool = True

class ChallengeCreate(ChallengeBase):
    pass

class ChallengeResponse(ChallengeBase):
    id: UUID
    created_at: datetime
    model_config = {"from_attributes": True}

class XPTransactionCreate(BaseModel):
    employee_id: UUID
    amount: int
    reason: str
    reference_id: Optional[UUID] = None

class XPTransactionResponse(XPTransactionCreate):
    id: UUID
    created_at: datetime
    model_config = {"from_attributes": True}

class LeaderboardEntry(BaseModel):
    rank: int
    employee_id: UUID
    total_xp: int
