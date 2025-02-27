import logging
import time

from fastapi import Request

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def logging_middleware(request: Request, call_next):
    """Log request timing and status code"""
    start_time = time.time()

    # Continue processing the request
    response = await call_next(request)

    # Log after request is processed
    duration = time.time() - start_time
    logger.info(
        f"Path: {request.url.path} "
        f"Duration: {duration:.2f}s "
        f"Status: {response.status_code}"
    )

    return response
