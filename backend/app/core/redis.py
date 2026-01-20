from redis.asyncio import Redis
from app.core.config import settings

_redis_client: Redis | None = None


async def get_redis() -> Redis:
    global _redis_client

    if _redis_client is None:
        _redis_client = Redis(
            host=settings.redis_host,
            port=settings.redis_port,
            db=settings.redis_db,
            decode_responses=True,
        )

    return _redis_client


async def close_redis() -> None:
    global _redis_client
    if _redis_client is not None:
        await _redis_client.close()
        _redis_client = None
