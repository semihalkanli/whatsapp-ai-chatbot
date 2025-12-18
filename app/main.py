"""
WhatsApp AI Chatbot - Main FastAPI Application
Multi-provider AI chatbot for WhatsApp Business API
"""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.config import settings
from app.routers import webhook

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level.upper()),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    logger.info("=" * 60)
    logger.info("WhatsApp AI Chatbot starting up...")
    logger.info(f"AI Provider: {settings.ai_provider}")
    logger.info(f"Debug Mode: {settings.debug}")
    logger.info("=" * 60)

    yield

    # Shutdown
    logger.info("WhatsApp AI Chatbot shutting down...")


# Create FastAPI application
app = FastAPI(
    title="WhatsApp AI Chatbot",
    description="Multi-provider AI chatbot for WhatsApp Business API (Groq, OpenAI, Claude)",
    version="1.0.0",
    lifespan=lifespan
)


# Include routers
app.include_router(webhook.router, tags=["webhook"])


@app.get("/")
async def root():
    """Root endpoint - health check."""
    return {
        "name": "WhatsApp AI Chatbot",
        "version": "1.0.0",
        "status": "running",
        "ai_provider": settings.ai_provider
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "ai_provider": settings.ai_provider,
        "debug": settings.debug
    }


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler."""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )
