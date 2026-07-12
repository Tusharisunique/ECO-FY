from sqlalchemy.orm import Session
from uuid import UUID
from .models import EmissionFactor, SustainabilityGoal
from .schemas import EmissionFactorCreate, SustainabilityGoalCreate, SustainabilityGoalUpdate

class EmissionFactorRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_all(self):
        return self.db.query(EmissionFactor).filter(EmissionFactor.is_active == True).all()

    def get_by_id(self, ef_id: UUID):
        return self.db.query(EmissionFactor).filter(EmissionFactor.id == ef_id).first()

    def create(self, data: EmissionFactorCreate):
        obj = EmissionFactor(**data.model_dump())
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete(self, obj: EmissionFactor):
        self.db.delete(obj)
        self.db.commit()

class SustainabilityGoalRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_by_org(self, organization_id: UUID):
        return self.db.query(SustainabilityGoal).filter(SustainabilityGoal.organization_id == organization_id).all()

    def get_by_id(self, goal_id: UUID):
        return self.db.query(SustainabilityGoal).filter(SustainabilityGoal.id == goal_id).first()

    def create(self, data: SustainabilityGoalCreate):
        obj = SustainabilityGoal(**data.model_dump())
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def update(self, goal: SustainabilityGoal, data: SustainabilityGoalUpdate):
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(goal, field, value)
        self.db.commit()
        self.db.refresh(goal)
        return goal

    def delete(self, obj: SustainabilityGoal):
        self.db.delete(obj)
        self.db.commit()
