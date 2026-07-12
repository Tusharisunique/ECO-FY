from sqlalchemy.orm import Session
from uuid import UUID
from datetime import datetime
from .models import CSRActivity, EmployeeParticipation
from .schemas import CSRActivityCreate, ParticipationCreate, ParticipationReview

class CSRActivityRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_by_org(self, organization_id: UUID):
        return self.db.query(CSRActivity).filter(CSRActivity.organization_id == organization_id).all()

    def get_by_id(self, activity_id: UUID):
        return self.db.query(CSRActivity).filter(CSRActivity.id == activity_id).first()

    def create(self, data: CSRActivityCreate):
        obj = CSRActivity(**data.model_dump())
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete(self, obj: CSRActivity):
        self.db.delete(obj)
        self.db.commit()

class ParticipationRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_pending(self, organization_id: UUID):
        return (
            self.db.query(EmployeeParticipation)
            .join(CSRActivity, EmployeeParticipation.csr_activity_id == CSRActivity.id)
            .filter(CSRActivity.organization_id == organization_id)
            .filter(EmployeeParticipation.status == "Pending")
            .all()
        )

    def list_by_employee(self, employee_id: UUID):
        return self.db.query(EmployeeParticipation).filter(
            EmployeeParticipation.employee_id == employee_id
        ).all()

    def get_by_id(self, participation_id: UUID):
        return self.db.query(EmployeeParticipation).filter(EmployeeParticipation.id == participation_id).first()

    def create(self, data: ParticipationCreate):
        obj = EmployeeParticipation(**data.model_dump())
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def review(self, participation: EmployeeParticipation, review: ParticipationReview):
        participation.status = review.status
        participation.reviewed_by = review.reviewed_by
        participation.reviewed_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(participation)
        return participation
