import uuid
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from core.database import SessionLocal
from modules.organization.models import Organization
from modules.organization.dept_employee_models import Department, Employee
from modules.auth.models import User
from modules.environmental.models import CarbonTransaction
from modules.social.models import CSRActivity, EmployeeParticipation
from modules.governance.models import Policy, Audit, ComplianceIssue
from modules.gamification.models import XPTransaction
from modules.esg_config.models import EmissionFactor
from core.security import get_password_hash

def run():
    db = SessionLocal()
    
    # 1. Clear out all the tables we are going to repopulate
    print("Clearing old demo data...")
    db.query(CarbonTransaction).delete()
    db.query(EmployeeParticipation).delete()
    db.query(CSRActivity).delete()
    db.query(Policy).delete()
    db.query(ComplianceIssue).delete()
    db.query(Audit).delete()
    db.query(XPTransaction).delete()
    # Delete dummy employees that are not the admin
    db.query(Employee).filter(Employee.role != "Admin").delete()
    db.query(User).filter(User.email != "admin@ecofy.com").delete()
    db.commit()

    print("Adding rich demo data...")
    # Get the admin org/user
    user = db.query(User).filter(User.email == "admin@ecofy.com").first()
    org = db.query(Organization).first()
    emp = db.query(Employee).filter(Employee.user_id == user.id).first()
    dept = db.query(Department).first()

    if not user or not org or not emp or not dept:
        print("Missing base org/user!")
        return

    now = datetime.utcnow()

    # Create dummy users for leaderboard
    dummy_users = []
    dummy_emps = []
    for i, name in enumerate(["Alex Chen", "Sarah Jenkins", "Michael Torres"]):
        u = User(email=f"dummy{i}@ecofy.com", hashed_password=get_password_hash("pass"), is_active=True)
        db.add(u)
        db.commit()
        dummy_users.append(u)
        e = Employee(user_id=u.id, department_id=dept.id, role="Employee")
        db.add(e)
        db.commit()
        dummy_emps.append(e)

    # 1. Carbon Transactions
    db.add_all([
        CarbonTransaction(employee_id=user.id, organization_id=org.id, activity_type="Scope 1: Fleet", quantity=450, unit="liters", co2e_kg=1035, activity_date=now - timedelta(days=5), description="Delivery route A"),
        CarbonTransaction(employee_id=user.id, organization_id=org.id, activity_type="Scope 1: Fleet", quantity=320, unit="liters", co2e_kg=736, activity_date=now - timedelta(days=12), description="Delivery route B"),
        CarbonTransaction(employee_id=user.id, organization_id=org.id, activity_type="Scope 2: Electricity", quantity=1500, unit="kWh", co2e_kg=1200, activity_date=now - timedelta(days=2), description="Main office power"),
        CarbonTransaction(employee_id=user.id, organization_id=org.id, activity_type="Scope 2: Electricity", quantity=2200, unit="kWh", co2e_kg=1760, activity_date=now - timedelta(days=30), description="Factory floor power"),
        CarbonTransaction(employee_id=user.id, organization_id=org.id, activity_type="Scope 3: Commute", quantity=1, unit="month", co2e_kg=150, activity_date=now - timedelta(days=15), description="Employee monthly commute"),
        CarbonTransaction(employee_id=user.id, organization_id=org.id, activity_type="Scope 3: Business Travel", quantity=1, unit="flight", co2e_kg=850, activity_date=now - timedelta(days=40), description="Conference flight (roundtrip)"),
        CarbonTransaction(employee_id=user.id, organization_id=org.id, activity_type="Scope 1: Heating", quantity=200, unit="therms", co2e_kg=1060, activity_date=now - timedelta(days=60), description="Winter office heating"),
    ])
    
    # 2. CSR Activities
    csr1 = CSRActivity(organization_id=org.id, title="Zero-Waste Office Initiative", description="Commit to sorting all office waste.", category="Environmental", xp_reward=200, is_active=True)
    csr2 = CSRActivity(organization_id=org.id, title="Local Park Cleanup", description="Saturday morning cleanup crew.", category="Community", xp_reward=150, is_active=True)
    csr3 = CSRActivity(organization_id=org.id, title="STEM Tutoring", description="Mentor local high school students in math.", category="Education", xp_reward=100, is_active=True)
    csr4 = CSRActivity(organization_id=org.id, title="Food Drive Volunteer", description="Sort donations at the local food bank.", category="Community", xp_reward=120, is_active=True)
    csr5 = CSRActivity(organization_id=org.id, title="Cycle to Work Month", description="Ditch the car for a whole month.", category="Environmental", xp_reward=300, is_active=True)
    
    db.add_all([csr1, csr2, csr3, csr4, csr5])
    db.commit()

    # 3. Participations
    db.add_all([
        EmployeeParticipation(csr_activity_id=csr1.id, employee_id=user.id, status="Approved", reviewed_at=now, hours_contributed=2.0),
        EmployeeParticipation(csr_activity_id=csr2.id, employee_id=user.id, status="Pending", hours_contributed=4.0),
        EmployeeParticipation(csr_activity_id=csr3.id, employee_id=user.id, status="Approved", reviewed_at=now, hours_contributed=1.5),
        EmployeeParticipation(csr_activity_id=csr1.id, employee_id=dummy_users[0].id, status="Approved", reviewed_at=now, hours_contributed=2.0),
    ])

    # 4. Gamification XP (for leaderboards)
    db.add_all([
        XPTransaction(employee_id=user.id, amount=200, reason="Completed: Zero-Waste Office"),
        XPTransaction(employee_id=user.id, amount=100, reason="Completed: STEM Tutoring"),
        XPTransaction(employee_id=user.id, amount=25, reason="Logged Carbon Emission"),
        XPTransaction(employee_id=user.id, amount=25, reason="Logged Carbon Emission"),
        XPTransaction(employee_id=user.id, amount=25, reason="Logged Carbon Emission"),
    ])
    db.add(XPTransaction(employee_id=dummy_users[0].id, amount=450, reason="Completed multiple activities"))
    db.add(XPTransaction(employee_id=dummy_users[1].id, amount=300, reason="Completed activities"))
    db.add(XPTransaction(employee_id=dummy_users[2].id, amount=150, reason="Completed activities"))

    # 5. Policies
    db.add_all([
        Policy(organization_id=org.id, title="Code of Ethics & Business Conduct", category="Ethics", version="2.1", is_active=True, effective_date=now - timedelta(days=365)),
        Policy(organization_id=org.id, title="Environmental Compliance Policy", category="Environment", version="1.3", is_active=True, effective_date=now - timedelta(days=200)),
        Policy(organization_id=org.id, title="Diversity & Inclusion Charter", category="HR", version="1.0", is_active=True, effective_date=now - timedelta(days=100)),
        Policy(organization_id=org.id, title="Data Privacy & Security", category="IT", version="3.0", is_active=True, effective_date=now - timedelta(days=50)),
        Policy(organization_id=org.id, title="Supplier Code of Conduct", category="Procurement", version="1.1", is_active=False, effective_date=now - timedelta(days=400)),
    ])
    
    # 6. Audits & Compliance Issues
    a1 = Audit(organization_id=org.id, title="Annual EHS Audit 2025", auditor="External Firm LLC", status="In Progress", start_date=now - timedelta(days=10))
    a2 = Audit(organization_id=org.id, title="Q2 Security & Privacy Review", auditor="Internal QA", status="Completed", start_date=now - timedelta(days=90), end_date=now - timedelta(days=85))
    a3 = Audit(organization_id=org.id, title="Supply Chain Sustainability", auditor="Internal QA", status="Scheduled", start_date=now + timedelta(days=30))
    db.add_all([a1, a2, a3])
    db.commit()

    db.add_all([
        ComplianceIssue(audit_id=a1.id, title="Waste disposal documentation gap", description="Missing manifest forms for Q1 hazardous waste.", severity="High", status="Open", due_date=now + timedelta(days=14)),
        ComplianceIssue(audit_id=a1.id, title="EHS training completion below 80%", description="Need to enforce mandatory training.", severity="Medium", status="Open", due_date=now + timedelta(days=21)),
        ComplianceIssue(audit_id=a1.id, title="Fire extinguisher inspection overdue", description="Building C extinguishers expired.", severity="Critical", status="Open", due_date=now + timedelta(days=2)),
        ComplianceIssue(audit_id=a2.id, title="Outdated employee access logs", description="Logs not rotated properly.", severity="Low", status="Resolved", resolved_at=now - timedelta(days=80)),
    ])
    
    db.commit()
    print("Database perfectly filled with rich demo data!")
    
if __name__ == "__main__":
    run()
