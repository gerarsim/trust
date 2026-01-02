from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.api.v1 import fraud, analysis
from app.ml.fraud_model import FraudDetector

# Global ML model instance
fraud_detector = FraudDetector()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await fraud_detector.load_models()
    print("✅ ML Models loaded successfully")
    yield
    # Shutdown
    print("🔄 Shutting down...")

app = FastAPI(
    title="TrustStep AI API",
    version="2.0.0",
    description="AI-powered fraud detection platform",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(fraud.router, prefix="/api/v1/fraud", tags=["fraud"])
app.include_router(analysis.router, prefix="/api/v1/analysis", tags=["analysis"])

@app.get("/")
async def root():
    return {
        "message": "TrustStep AI API",
        "version": "2.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}
