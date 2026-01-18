from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.logging import setup_logging, get_logger, setup_audit_log_file
from app.api.decision import router as decision_router
from app.api.ingestion import router as ingestion_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    setup_audit_log_file()

    logger = get_logger()
    logger.info(
        "application_startup",
        service="backend",
        environment=settings.app_env,
    )

    yield

    logger.info(
        "application_shutdown",
        service="backend",
        environment=settings.app_env,
    )


app = FastAPI(
    title="Enterprise Financial Decision Assistant",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(decision_router)
app.include_router(ingestion_router)


@app.get("/health", tags=["system"])
async def health_check():
    return {
        "status": "ok",
        "service": "backend",
        "environment": settings.app_env,
    }
