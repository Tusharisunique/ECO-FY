from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional

class CSRActivityBase(BaseModel):
    organization_id: UUID
    title: str
    description: Optional[str] = None
    category: str
    xp_reward: int = 50
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    is_active: bool = True

class CSRActivityCreate(CSRActivityBase):
    pass

class CSRActivityResponse(CSRActivityBase):
    id: UUID
    created_at: datetime
    model_config = {"from_attributes": True}

class ParticipationBase(BaseModel):
    csr_activity_id: UUID
    employee_id: UUID
    hours_contributed: float = 0.0
    notes: Optional[str] = None
    evidence_url: Optional[str] = None

class ParticipationCreate(ParticipationBase):
    pass

class ParticipationReview(BaseModel):
    status: str  # Approved | Rejected
    reviewed_by: UUID

class ParticipationResponse(ParticipationBase):
    id: UUID
    status: str
    reviewed_by: Optional[UUID] = None
    reviewed_at: Optional[datetime] = None
    created_at: datetime
    model_config = {"from_attributes": True}
