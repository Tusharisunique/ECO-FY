from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from typing import Optional
from datetime import datetime
from core.database import get_db
from core.dependencies import get_current_active_user
from .repository import CarbonTransactionRepository, CarbonCalculationService
from .schemas import (
    CarbonTransactionCreate, CarbonTransactionResponse,
    EmissionCalculationRequest, EmissionCalculationResponse
)

router = APIRouter()

@router.get("/carbon-transactions", response_model=list[CarbonTransactionResponse])
def list_transactions(
    organization_id: UUID,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db),
    _=Depends(get_current_active_user),
):
    return CarbonTransactionRepository(db).list_by_org(organization_id, start_date, end_date)

@router.post("/carbon-transactions", response_model=CarbonTransactionResponse, status_code=201)
def log_carbon_transaction(
    data: CarbonTransactionCreate,
    db: Session = Depends(get_db),
    _=Depends(get_current_active_user),
):
    repo = CarbonTransactionRepository(db)
    co2e_kg = 0.0
    if data.emission_factor_id:
        ef = repo.get_emission_factor(data.emission_factor_id)
        if not ef:
            raise HTTPException(status_code=404, detail="Emission factor not found")
        co2e_kg = CarbonCalculationService.calculate_co2e(data.quantity, ef.co2e_per_unit)
    return repo.create(data, co2e_kg)

@router.get("/carbon-transactions/{txn_id}", response_model=CarbonTransactionResponse)
def get_transaction(txn_id: UUID, db: Session = Depends(get_db), _=Depends(get_current_active_user)):
    txn = CarbonTransactionRepository(db).get_by_id(txn_id)
    if not txn:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return txn

@router.delete("/carbon-transactions/{txn_id}", status_code=204)
def delete_transaction(txn_id: UUID, db: Session = Depends(get_db), _=Depends(get_current_active_user)):
    repo = CarbonTransactionRepository(db)
    txn = repo.get_by_id(txn_id)
    if not txn:
        raise HTTPException(status_code=404, detail="Transaction not found")
    repo.delete(txn)

@router.post("/calculate-emission", response_model=EmissionCalculationResponse)
def calculate_emission(
    data: EmissionCalculationRequest,
    db: Session = Depends(get_db),
    _=Depends(get_current_active_user),
):
    repo = CarbonTransactionRepository(db)
    ef = repo.get_emission_factor(data.emission_factor_id)
    if not ef:
        raise HTTPException(status_code=404, detail="Emission factor not found")
    co2e_kg = CarbonCalculationService.calculate_co2e(data.quantity, ef.co2e_per_unit)
    return EmissionCalculationResponse(
        emission_factor_name=ef.name,
        quantity=data.quantity,
        unit=ef.unit,
        co2e_kg=co2e_kg,
        co2e_tonnes=round(co2e_kg / 1000, 6),
    )

@router.get("/carbon-summary")
def carbon_summary(organization_id: UUID, db: Session = Depends(get_db), _=Depends(get_current_active_user)):
    repo = CarbonTransactionRepository(db)
    total_kg = repo.total_co2e_by_org(organization_id)
    return {
        "organization_id": str(organization_id),
        "total_co2e_kg": total_kg,
        "total_co2e_tonnes": round(total_kg / 1000, 4),
    }
