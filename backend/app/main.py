from fastapi import FastAPI
from app.api.decision import router as decision_router
from app.api.ingestion import router as ingestion_router
from app.core.logging import get_logger

logger = get_logger("efda")

app = FastAPI(title="Enterprise Financial Decision Assistant")

@app.get("/health")
async def health():
    return {"status": "ok"}

app.include_router(decision_router, prefix="/decision", tags=["Decision"])
app.include_router(ingestion_router, prefix="/ingestion", tags=["Ingestion"])

@app.on_event("startup")
async def startup_event():
    logger.info("Backend started successfully")
