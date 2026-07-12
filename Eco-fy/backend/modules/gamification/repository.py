from sqlalchemy import func
from sqlalchemy.orm import Session
from uuid import UUID
from .models import Badge, EmployeeBadge, Reward, Challenge, XPTransaction
from .schemas import BadgeCreate, RewardCreate, ChallengeCreate, XPTransactionCreate

class BadgeRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_by_org(self, organization_id: UUID):
        return self.db.query(Badge).filter(Badge.organization_id == organization_id).all()

    def get_by_id(self, badge_id: UUID):
        return self.db.query(Badge).filter(Badge.id == badge_id).first()

    def create(self, data: BadgeCreate):
        obj = Badge(**data.model_dump())
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def award_to_employee(self, employee_id: UUID, badge_id: UUID):
        obj = EmployeeBadge(employee_id=employee_id, badge_id=badge_id)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def list_employee_badges(self, employee_id: UUID):
        return self.db.query(EmployeeBadge).filter(EmployeeBadge.employee_id == employee_id).all()

class RewardRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_by_org(self, organization_id: UUID):
        return self.db.query(Reward).filter(Reward.organization_id == organization_id, Reward.is_active == True).all()

    def get_by_id(self, reward_id: UUID):
        return self.db.query(Reward).filter(Reward.id == reward_id).first()

    def create(self, data: RewardCreate):
        obj = Reward(**data.model_dump())
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

class ChallengeRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_by_org(self, organization_id: UUID):
        return self.db.query(Challenge).filter(Challenge.organization_id == organization_id).all()

    def get_by_id(self, challenge_id: UUID):
        return self.db.query(Challenge).filter(Challenge.id == challenge_id).first()

    def create(self, data: ChallengeCreate):
        obj = Challenge(**data.model_dump())
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

class XPRepository:
    def __init__(self, db: Session):
        self.db = db

    def award(self, data: XPTransactionCreate):
        obj = XPTransaction(**data.model_dump())
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def get_employee_total_xp(self, employee_id: UUID) -> int:
        result = self.db.query(func.sum(XPTransaction.amount)).filter(
            XPTransaction.employee_id == employee_id
        ).scalar()
        return result or 0

    def get_leaderboard(self, organization_id: UUID, limit: int = 10):
        from modules.organization.dept_employee_models import Employee, Department
        results = (
            self.db.query(
                XPTransaction.employee_id,
                func.sum(XPTransaction.amount).label("total_xp"),
            )
            .join(Employee, XPTransaction.employee_id == Employee.id)
            .join(Department, Employee.department_id == Department.id)
            .filter(Department.organization_id == organization_id)
            .group_by(XPTransaction.employee_id)
            .order_by(func.sum(XPTransaction.amount).desc())
            .limit(limit)
            .all()
        )
        return [{"rank": i + 1, "employee_id": r[0], "total_xp": r[1] or 0} for i, r in enumerate(results)]
