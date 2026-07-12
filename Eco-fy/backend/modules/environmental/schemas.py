from pydantic import BaseModel, field_validator
from uuid import UUID
from datetime import datetime
from typing import Optional

class CarbonTransactionBase(BaseModel):
    employee_id: UUID
    organization_id: Optional[UUID] = None
    emission_factor_id: Optional[UUID] = None
    activity_type: str
    description: Optional[str] = None
    quantity: float
    unit: str
    activity_date: datetime
    notes: Optional[str] = None

class CarbonTransactionCreate(CarbonTransactionBase):
    pass

class CarbonTransactionResponse(CarbonTransactionBase):
    id: UUID
    co2e_kg: float
    created_at: datetime
    model_config = {"from_attributes": True}

class EmissionCalculationRequest(BaseModel):
    emission_factor_id: UUID
    quantity: float

class EmissionCalculationResponse(BaseModel):
    emission_factor_name: str
    quantity: float
    unit: str
    co2e_kg: float
    co2e_tonnes: float
