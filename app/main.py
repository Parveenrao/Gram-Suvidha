
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.database import engine, Base
from app.routers import auth, budget, project, announcement, grievance, document, village
from app.middleware.auth_middleware import AuthMiddleware, LoggingMiddleware
from app.utils.logging import get_logger

logger = get_logger(__name__)


# ─────────────────────────────────────────
# CREATE TABLES AUTOMATICALLY (NO ALEMBIC)
# ─────────────────────────────────────────
Base.metadata.create_all(bind=engine)



# ─────────────────────────────────────────
# LIFESPAN (startup + shutdown replacement)
# ─────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("-----------------------------")
    logger.info(" GramSuvidha API Starting...")

    # Create tables automatically (since no Alembic)
    Base.metadata.create_all(bind=engine)
    logger.info(" Database tables created")

    yield  # Application runs here

    # Shutdown
    logger.info(" GramSuvidha API Shutting Down...")
    logger.info("---------------------------------")


# ─────────────────────────────────────────
# FastAPI App
# ─────────────────────────────────────────
app = FastAPI(
    title="🏘️ GramSuvidha — Village Panchayat App",
    version="1.0.0",
    lifespan=lifespan
)

# ─────────────────────────────────────────
# MIDDLEWARE
# ─────────────────────────────────────────
app.add_middleware(AuthMiddleware)
app.add_middleware(LoggingMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─────────────────────────────────────────
# ROUTERS
# ─────────────────────────────────────────
app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(village.router, prefix="/api/villages", tags=["Villages"])
app.include_router(budget.router, prefix="/api/budget", tags=["Budget"])
app.include_router(project.router, prefix="/api/projects", tags=["Projects"])
app.include_router(announcement.router, prefix="/api/announcements", tags=["Announcements"])
app.include_router(grievance.router, prefix="/api/grievances", tags=["Grievances"])
app.include_router(document.router, prefix="/api/documents", tags=["Documents"])

# ─────────────────────────────────────────
# HEALTH CHECK
# ─────────────────────────────────────────
@app.get("/")
def root():
    return {"status": "running"}

@app.get("/health")
def health():
    return {"status": "healthy"}


