from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from typing import Optional
from datetime import datetime
from core.database import get_db
from core.dependencies import get_current_active_user
from .repository import CarbonTransactionRepository, CarbonCalculationService
from .models import CarbonTransaction
from .schemas import (
    CarbonTransactionCreate, CarbonTransactionResponse,
    EmissionCalculationRequest, EmissionCalculationResponse
)

router = APIRouter()

@router.get("/carbon-transactions", response_model=list[CarbonTransactionResponse])
def list_transactions(
    organization_id: Optional[UUID] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db),
    _=Depends(get_current_active_user),
):
    # If organization_id is not provided, we can fetch all or handle appropriately
    if organization_id:
        return CarbonTransactionRepository(db).list_by_org(organization_id, start_date, end_date)
    
    # For demo purposes, returning all transactions if org_id is not passed
    return db.query(CarbonTransaction).all()

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
    else:
        # Fallback calculation for demo if no emission factor is provided
        if "Scope 1" in data.activity_type:
            co2e_kg = float(data.quantity) * 2.3
        elif "Scope 2" in data.activity_type:
            co2e_kg = float(data.quantity) * 0.8
        else:
            co2e_kg = float(data.quantity) * 1.5
            
    txn = repo.create(data, co2e_kg)
    
    # Award XP for logging carbon emissions
    if data.employee_id:
        try:
            from modules.gamification.repository import XPRepository
            from modules.gamification.schemas import XPTransactionCreate
            xp_repo = XPRepository(db)
            xp_repo.award(XPTransactionCreate(
                employee_id=data.employee_id,
                amount=25,
                reason=f"Logged Carbon Emission: {data.activity_type}"
            ))
        except Exception as e:
            print(f"Failed to award XP: {e}")
            
    return txn

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
def carbon_summary(organization_id: Optional[UUID] = None, db: Session = Depends(get_db), _=Depends(get_current_active_user)):
    repo = CarbonTransactionRepository(db)
    
    # If no org provided, just return total for all or demo default
    if organization_id:
        total_kg = repo.total_co2e_by_org(organization_id)
    else:
        # Fallback for demo without org
        txs = db.query(CarbonTransaction).all()
        total_kg = sum(tx.co2e_kg for tx in txs if tx.co2e_kg)

    return {
        "organization_id": str(organization_id),
        "total_co2e_kg": total_kg,
        "total_co2e_tonnes": round(total_kg / 1000, 4),
    }
