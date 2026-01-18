from app.db.session import engine
from app.db.models.base import Base

# Import all models so metadata is registered
from app.db.models.audit_log import AuditLog  # noqa: F401


async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
