from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from core.config import settings

# --- Module Routers ---
from modules.auth.routes import router as auth_router
from modules.organization.routes import router as org_router
from modules.esg_config.routes import router as esg_config_router
from modules.environmental.routes import router as environmental_router
from modules.social.routes import router as social_router
from modules.governance.routes import router as governance_router
from modules.gamification.routes import router as gamification_router
from modules.ai.routes import router as ai_router
from modules.upload.routes import router as upload_router
from modules.analytics.routes import router as analytics_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="AI-Powered ESG Operating System",
    version="1.0.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# --- Register Routers ---
API = settings.API_V1_STR
app.include_router(auth_router,          prefix=f"{API}/auth",          tags=["Auth"])
app.include_router(org_router,           prefix=f"{API}/org",            tags=["Organization"])
app.include_router(esg_config_router,    prefix=f"{API}/esg-config",     tags=["ESG Config"])
app.include_router(environmental_router, prefix=f"{API}/environmental",   tags=["Environmental"])
app.include_router(social_router,        prefix=f"{API}/social",          tags=["Social"])
app.include_router(governance_router,    prefix=f"{API}/governance",      tags=["Governance"])
app.include_router(gamification_router,  prefix=f"{API}/gamification",    tags=["Gamification"])
app.include_router(ai_router,            prefix=f"{API}/ai",              tags=["AI"])
app.include_router(upload_router,        prefix=f"{API}/upload",          tags=["Upload"])
app.include_router(analytics_router,     prefix=f"{API}/analytics",       tags=["Analytics"])

@app.get("/", tags=["Health"])
def health_check():
    return {"status": "ok", "service": settings.PROJECT_NAME}
