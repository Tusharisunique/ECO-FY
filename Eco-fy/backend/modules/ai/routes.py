from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from openai import OpenAI
from pydantic import BaseModel

from core.database import get_db
from core.config import settings
from core.dependencies import get_current_active_user
from modules.auth.models import User
from modules.environmental.models import CarbonTransaction
from modules.social.models import CSRActivity

router = APIRouter()

# Initialize OpenAI client with OpenRouter base URL
client = OpenAI(
    base_url=settings.OPENROUTER_BASE_URL,
    api_key=settings.OPENROUTER_API_KEY,
)

class AIInsightResponse(BaseModel):
    insights: str

@router.get("/insights", response_model=AIInsightResponse)
def get_ai_insights(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Generate ESG insights using OpenRouter AI based on the organization's real data.
    """
    # Fetch real data for context
    emissions = db.query(CarbonTransaction).limit(50).all()
    csr_activities = db.query(CSRActivity).limit(20).all()

    total_emissions = sum([e.co2e_kg for e in emissions])
    active_csr = len([c for c in csr_activities if c.is_active])

    # Build prompt context
    prompt = f"""
    You are an expert ESG (Environmental, Social, Governance) analyst.
    I am looking for a brief executive summary of our current ESG performance and actionable recommendations.
    
    Here is our current data:
    - Total Carbon Emissions: {total_emissions} tons CO2e
    - Number of Active CSR Activities: {active_csr}
    
    Please provide:
    1. A short analysis of our carbon footprint.
    2. A recommendation to improve our Social initiatives based on {active_csr} active projects.
    3. One general Governance best practice.
    
    Keep it concise, professional, and directly actionable (under 200 words).
    """

    try:
        response = client.chat.completions.create(
            model=settings.AI_MODEL,
            messages=[
                {"role": "system", "content": "You are a top-tier ESG consultant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
        )
        insight_text = response.choices[0].message.content
        return {"insights": insight_text}
    except Exception as e:
        return {"insights": f"Unable to generate AI insights at this time. Error: {str(e)}"}
