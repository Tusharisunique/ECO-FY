from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional

class EmissionFactorBase(BaseModel):
    name: str
    category: str
    unit: str
    co2e_per_unit: float
    source: Optional[str] = None
    is_active: bool = True

class EmissionFactorCreate(EmissionFactorBase):
    pass

class EmissionFactorResponse(EmissionFactorBase):
    id: UUID
    created_at: datetime
    model_config = {"from_attributes": True}

class SustainabilityGoalBase(BaseModel):
    organization_id: UUID
    title: str
    description: Optional[str] = None
    category: str
    target_value: float
    current_value: float = 0.0
    unit: str
    target_date: datetime
    status: str = "Active"

class SustainabilityGoalCreate(SustainabilityGoalBase):
    pass

class SustainabilityGoalUpdate(BaseModel):
    current_value: Optional[float] = None
    status: Optional[str] = None
    description: Optional[str] = None

class SustainabilityGoalResponse(SustainabilityGoalBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}
