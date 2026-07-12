from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from uuid import UUID
from typing import Optional
from datetime import datetime, timedelta
from core.database import get_db
from core.dependencies import get_current_active_user

router = APIRouter()

@router.get("/dashboard")
def get_dashboard_data(organization_id: Optional[UUID] = None, db: Session = Depends(get_db), _=Depends(get_current_active_user)):
    from modules.environmental.models import CarbonTransaction
    from modules.social.models import CSRActivity, EmployeeParticipation
    from modules.governance.models import ComplianceIssue
    from modules.gamification.models import XPTransaction
    from modules.auth.models import User

    # 1. Carbon trend: group transactions by month
    txs = db.query(CarbonTransaction).all()
    monthly: dict = {}
    for t in txs:
        month = t.activity_date.strftime("%b %Y")
        monthly[month] = monthly.get(month, 0) + (t.co2e_kg or 0)
    # Sort chronologically
    sorted_months = sorted(monthly.items(), key=lambda x: datetime.strptime(x[0], "%b %Y"))
    carbon_data = [{"month": m, "value": round(v / 1000, 2)} for m, v in sorted_months]

    # 2. ESG breakdown scores (computed from real DB)
    total_co2e = sum(t.co2e_kg or 0 for t in txs)
    # Env score: lower emissions = higher score (max 100)
    env_score = max(0, round(100 - min(total_co2e / 500, 100)))

    all_participations = db.query(EmployeeParticipation).filter(EmployeeParticipation.status == "Approved").count()
    social_score = min(100, all_participations * 20)  # 5 approved = 100

    open_issues = db.query(ComplianceIssue).filter(ComplianceIssue.status == "Open").count()
    gov_score = max(0, 100 - open_issues * 10)  # each open issue reduces score

    esg_breakdown = [
        {"name": "Environmental", "value": env_score, "color": "#355C4D"},
        {"name": "Social", "value": social_score, "color": "#7A8B68"},
        {"name": "Governance", "value": gov_score, "color": "#D8C7A3"},
    ]

    # 3. Recent activity feed from XP transactions
    recent_xp = db.query(XPTransaction, User).join(User, XPTransaction.employee_id == User.id).order_by(XPTransaction.created_at.desc()).limit(5).all()
    recent_activities = []
    for xp, user in recent_xp:
        name = f"{user.first_name or ''} {user.last_name or ''}".strip() or user.email.split('@')[0]
        delta = datetime.utcnow() - xp.created_at
        if delta.days > 0:
            time_str = f"{delta.days}d ago"
        elif delta.seconds // 3600 > 0:
            time_str = f"{delta.seconds // 3600}h ago"
        else:
            time_str = "Just now"
        recent_activities.append({
            "id": str(xp.id),
            "user": name,
            "action": xp.reason,
            "xp": f"+{xp.amount} XP",
            "time": time_str
        })

    # 4. Sustainability goals
    total_txs = len(txs)
    from modules.governance.models import Policy as PolicyModel
    total_policies = db.query(PolicyModel).count()
    goals = [
        {"name": "Reduce Scope 1 Emissions by 30%", "current": min(100, max(0, 100 - int(sum(t.co2e_kg for t in txs if 'Scope 1' in t.activity_type) / 50)))},
        {"name": "CSR Activity Participation", "current": min(100, all_participations * 25)},
        {"name": "Policy Compliance", "current": min(100, total_policies * 20)},
        {"name": "Carbon Transactions Logged", "current": min(100, total_txs * 10)},
    ]

    # 5. Top-level KPIs
    total_co2_tonnes = round(total_co2e / 1000, 2)
    active_users = db.query(User).filter(User.is_active == True).count()

    return {
        "carbonData": carbon_data,
        "esgBreakdown": esg_breakdown,
        "recentActivities": recent_activities,
        "goals": goals,
        "kpis": {
            "total_co2e_tonnes": total_co2_tonnes,
            "active_employees": active_users,
            "open_issues": open_issues,
            "esg_score": round((env_score + social_score + gov_score) / 3)
        }
    }

@router.get("/trends")
def get_trends_data(organization_id: Optional[UUID] = None, db: Session = Depends(get_db), _=Depends(get_current_active_user)):
    return {
        "esgTrend": [],
        "radarData": []
    }
