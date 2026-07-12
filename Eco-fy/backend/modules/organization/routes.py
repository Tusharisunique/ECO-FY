from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from core.database import get_db
from core.dependencies import get_current_active_user
from .repository import OrganizationRepository, DepartmentRepository, EmployeeRepository
from .schemas import (
    OrganizationCreate, OrganizationResponse,
    DepartmentCreate, DepartmentResponse,
    EmployeeCreate, EmployeeResponse
)

router = APIRouter()

# --- Organizations ---
@router.get("/organizations", response_model=list[OrganizationResponse])
def list_organizations(db: Session = Depends(get_db), _=Depends(get_current_active_user)):
    return OrganizationRepository(db).list_organizations()

@router.post("/organizations", response_model=OrganizationResponse, status_code=201)
def create_organization(data: OrganizationCreate, db: Session = Depends(get_db), _=Depends(get_current_active_user)):
    return OrganizationRepository(db).create(data)

@router.get("/organizations/{org_id}", response_model=OrganizationResponse)
def get_organization(org_id: UUID, db: Session = Depends(get_db), _=Depends(get_current_active_user)):
    org = OrganizationRepository(db).get_by_id(org_id)
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    return org

@router.delete("/organizations/{org_id}", status_code=204)
def delete_organization(org_id: UUID, db: Session = Depends(get_db), _=Depends(get_current_active_user)):
    repo = OrganizationRepository(db)
    org = repo.get_by_id(org_id)
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    repo.delete(org)

# --- Departments ---
@router.get("/departments", response_model=list[DepartmentResponse])
def list_departments(organization_id: UUID, db: Session = Depends(get_db), _=Depends(get_current_active_user)):
    return DepartmentRepository(db).list_by_org(organization_id)

@router.post("/departments", response_model=DepartmentResponse, status_code=201)
def create_department(data: DepartmentCreate, db: Session = Depends(get_db), _=Depends(get_current_active_user)):
    return DepartmentRepository(db).create(data)

@router.get("/departments/{dept_id}", response_model=DepartmentResponse)
def get_department(dept_id: UUID, db: Session = Depends(get_db), _=Depends(get_current_active_user)):
    dept = DepartmentRepository(db).get_by_id(dept_id)
    if not dept:
        raise HTTPException(status_code=404, detail="Department not found")
    return dept

@router.delete("/departments/{dept_id}", status_code=204)
def delete_department(dept_id: UUID, db: Session = Depends(get_db), _=Depends(get_current_active_user)):
    repo = DepartmentRepository(db)
    dept = repo.get_by_id(dept_id)
    if not dept:
        raise HTTPException(status_code=404, detail="Department not found")
    repo.delete(dept)

# --- Employees ---
@router.get("/employees", response_model=list[EmployeeResponse])
def list_employees(department_id: UUID, db: Session = Depends(get_db), _=Depends(get_current_active_user)):
    return EmployeeRepository(db).list_by_dept(department_id)

@router.post("/employees", response_model=EmployeeResponse, status_code=201)
def create_employee(data: EmployeeCreate, db: Session = Depends(get_db), _=Depends(get_current_active_user)):
    return EmployeeRepository(db).create(data)
