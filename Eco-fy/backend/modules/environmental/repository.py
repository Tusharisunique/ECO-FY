from sqlalchemy.orm import Session
from uuid import UUID
from datetime import datetime
from typing import Optional
from .models import CarbonTransaction
from .schemas import CarbonTransactionCreate
from modules.esg_config.models import EmissionFactor

class CarbonCalculationService:
    """Pure business logic for emission calculations. No DB access."""

    @staticmethod
    def calculate_co2e(quantity: float, co2e_per_unit: float) -> float:
        """Returns kg CO2e for a given quantity and emission factor."""
        return round(quantity * co2e_per_unit, 4)

class CarbonTransactionRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_by_org(self, organization_id: UUID, start: Optional[datetime] = None, end: Optional[datetime] = None):
        query = self.db.query(CarbonTransaction).filter(CarbonTransaction.organization_id == organization_id)
        if start:
            query = query.filter(CarbonTransaction.activity_date >= start)
        if end:
            query = query.filter(CarbonTransaction.activity_date <= end)
        return query.order_by(CarbonTransaction.activity_date.desc()).all()

    def list_by_employee(self, employee_id: UUID):
        return self.db.query(CarbonTransaction).filter(
            CarbonTransaction.employee_id == employee_id
        ).order_by(CarbonTransaction.activity_date.desc()).all()

    def get_by_id(self, txn_id: UUID):
        return self.db.query(CarbonTransaction).filter(CarbonTransaction.id == txn_id).first()

    def get_emission_factor(self, ef_id: UUID):
        return self.db.query(EmissionFactor).filter(EmissionFactor.id == ef_id).first()

    def create(self, data: CarbonTransactionCreate, co2e_kg: float):
        obj = CarbonTransaction(**data.model_dump(), co2e_kg=co2e_kg)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def total_co2e_by_org(self, organization_id: UUID) -> float:
        from sqlalchemy import func
        result = self.db.query(func.sum(CarbonTransaction.co2e_kg)).filter(
            CarbonTransaction.organization_id == organization_id
        ).scalar()
        return result or 0.0

    def delete(self, obj: CarbonTransaction):
        self.db.delete(obj)
        self.db.commit()
