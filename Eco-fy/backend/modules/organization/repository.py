from sqlalchemy.orm import Session
from uuid import UUID
from .models import Organization
from .dept_employee_models import Department, Employee
from .schemas import OrganizationCreate, DepartmentCreate, EmployeeCreate

class OrganizationRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_organizations(self):
        return self.db.query(Organization).all()

    def get_by_id(self, org_id: UUID):
        return self.db.query(Organization).filter(Organization.id == org_id).first()

    def create(self, data: OrganizationCreate):
        obj = Organization(**data.model_dump())
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete(self, org: Organization):
        self.db.delete(org)
        self.db.commit()

class DepartmentRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_by_org(self, organization_id: UUID):
        return self.db.query(Department).filter(Department.organization_id == organization_id).all()

    def get_by_id(self, dept_id: UUID):
        return self.db.query(Department).filter(Department.id == dept_id).first()

    def create(self, data: DepartmentCreate):
        obj = Department(**data.model_dump())
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete(self, dept: Department):
        self.db.delete(dept)
        self.db.commit()

class EmployeeRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_by_dept(self, department_id: UUID):
        return self.db.query(Employee).filter(Employee.department_id == department_id).all()

    def get_by_user_id(self, user_id: UUID):
        return self.db.query(Employee).filter(Employee.user_id == user_id).first()

    def get_by_id(self, employee_id: UUID):
        return self.db.query(Employee).filter(Employee.id == employee_id).first()

    def create(self, data: EmployeeCreate):
        obj = Employee(**data.model_dump())
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj
