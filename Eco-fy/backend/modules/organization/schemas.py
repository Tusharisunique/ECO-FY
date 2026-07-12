from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional

class OrganizationBase(BaseModel):
    name: str
    industry: Optional[str] = None
    country: Optional[str] = None
    website: Optional[str] = None

class OrganizationCreate(OrganizationBase):
    pass

class OrganizationResponse(OrganizationBase):
    id: UUID
    created_at: datetime
    model_config = {"from_attributes": True}

class DepartmentBase(BaseModel):
    name: str
    organization_id: UUID

class DepartmentCreate(DepartmentBase):
    pass

class DepartmentResponse(DepartmentBase):
    id: UUID
    created_at: datetime
    model_config = {"from_attributes": True}

class EmployeeBase(BaseModel):
    user_id: UUID
    department_id: UUID
    role: Optional[str] = "Employee"

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeResponse(EmployeeBase):
    id: UUID
    created_at: datetime
    model_config = {"from_attributes": True}
