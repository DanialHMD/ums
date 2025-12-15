import logging
from typing import Optional

from redis.asyncio import Redis, from_url

from app.core.settings import Settings

settings = Settings()
logger = logging.getLogger("__name__")

redis_client: Optional[Redis] = None

async def init_redis_pool() -> None:
    global redis_client
    redis_url = settings.REDIS_URL
    if not redis_url:
        logger.info("REDIS_URL not configured, skipping Redis init")
        return
    redis_client = from_url(redis_url, decode_responses=True)
    try:
        await redis_client.ping()
        logger.info("Connected to Redis at %s", redis_url)
    except Exception:
        logger.exception("Failed connecting to Redis")
        # ensure client cleaned up on failure
        try:
            await redis_client.close()
            await redis_client.connection_pool.disconnect()
        except Exception:
            pass
        redis_client = None
        raise

async def close_redis_pool() -> None:
    global redis_client
    if redis_client:
        try:
            await redis_client.close()
            await redis_client.connection_pool.disconnect()
            logger.info("Redis connection closed")
        except Exception:
            pass

def get_redis_client() -> Optional[Redis]:
    return redis_client