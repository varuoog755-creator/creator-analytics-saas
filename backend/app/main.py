"""
Creator Analytics SaaS - Main FastAPI Application
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import structlog

from app.core.config import settings
from app.api.auth import router as auth_router
from app.api.users import router as users_router
from app.api.analytics import router as analytics_router
from app.api.predictions import router as predictions_router
from app.api.platforms import router as platforms_router
from app.api.reports import router as reports_router
from app.api.dashboard import router as dashboard_router
from app.ml.router import router as ml_router

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.add_log_level,
        structlog.stdlib.filter_by_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.dev.ConsoleRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True
)

logger = structlog.get_logger()

app = FastAPI(
    title="Creator Analytics API",
    description="Advanced Multi-Platform Creator Analytics & Predictions",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Exception handlers
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error("Unhandled exception", exc_info=exc)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )


# Health check
@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}


@app.get("/")
async def root():
    return {
        "name": "Creator Analytics SaaS",
        "version": "1.0.0",
        "docs": "/docs"
    }


# Include routers
app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])
app.include_router(users_router, prefix="/api/users", tags=["Users"])
app.include_router(platforms_router, prefix="/api/platforms", tags=["Platforms"])
app.include_router(analytics_router, prefix="/api/analytics", tags=["Analytics"])
app.include_router(predictions_router, prefix="/api/predict", tags=["Predictions"])
app.include_router(reports_router, prefix="/api/reports", tags=["Reports"])
app.include_router(dashboard_router, prefix="/api/dashboard", tags=["Dashboard"])
app.include_router(ml_router, prefix="/api/ml", tags=["ML Models"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
