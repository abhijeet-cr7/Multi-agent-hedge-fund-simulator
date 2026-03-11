"""
Redis queue worker for processing BullMQ jobs from NestJS.
Listens to the 'agent-analysis' queue and calls agent analysis.
"""
import json
import asyncio
import logging
import redis
import httpx
from config import settings

logging.basicConfig(level=settings.log_level)
logger = logging.getLogger(__name__)

QUEUE_KEY = "bull:agent-analysis:wait"


async def process_job(job_data: dict) -> None:
    """Process a single analysis job."""
    symbol = job_data.get("symbol", "").upper()
    agent_type = job_data.get("agentType", "all")

    logger.info(f"Processing job: symbol={symbol}, agent_type={agent_type}")

    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                f"{settings.python_ai_url}/analyze",
                json={"symbol": symbol, "agent_type": agent_type},
            )
            logger.info(f"Analysis completed for {symbol}: {response.status_code}")
    except Exception as e:
        logger.error(f"Failed to process job for {symbol}: {e}")


def start_worker() -> None:
    """Start the Redis queue worker."""
    r = redis.from_url(settings.redis_url, decode_responses=True)
    logger.info(f"Worker started, listening to {QUEUE_KEY}")

    while True:
        try:
            result = r.blpop(QUEUE_KEY, timeout=5)
            if result:
                _, raw = result
                job = json.loads(raw)
                job_data = job.get("data", job)
                asyncio.run(process_job(job_data))
        except redis.exceptions.ConnectionError as e:
            logger.error(f"Redis connection error: {e}")
            import time
            time.sleep(5)
        except Exception as e:
            logger.error(f"Worker error: {e}")


if __name__ == "__main__":
    start_worker()
