import asyncio
from sqlalchemy.orm import Session
from core.database import SessionLocal, engine, Base
from core.security import get_password_hash
from modules.auth.models import User
from modules.organization.models import Organization
from modules.organization.dept_employee_models import Department, Employee

def seed_db():
    db = SessionLocal()
    try:
        # Check if user exists
        user = db.query(User).filter(User.email == "admin@ecofy.com").first()
        if not user:
            print("Creating admin user...")
            hashed_password = get_password_hash("admin123")
            user = User(email="admin@ecofy.com", hashed_password=hashed_password, is_active=True, is_superuser=True)
            db.add(user)
            db.commit()
            db.refresh(user)

        # Check if org exists
        org = db.query(Organization).filter(Organization.name == "Eco-fy Demo Org").first()
        if not org:
            print("Creating organization...")
            org = Organization(name="Eco-fy Demo Org", industry="Technology", country="USA")
            db.add(org)
            db.commit()
            db.refresh(org)

        # Check if dept exists
        dept = db.query(Department).filter(Department.name == "Engineering").first()
        if not dept:
            print("Creating department...")
            dept = Department(name="Engineering", organization_id=org.id)
            db.add(dept)
            db.commit()
            db.refresh(dept)

        # Check if employee exists
        emp = db.query(Employee).filter(Employee.user_id == user.id).first()
        if not emp:
            print("Creating employee...")
            emp = Employee(user_id=user.id, department_id=dept.id, role="Admin")
            db.add(emp)
            db.commit()

        print("Database seeded successfully!")
    except Exception as e:
        print(f"Error seeding DB: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_db()
