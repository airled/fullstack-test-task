import uuid
import asyncio
import os
from celery import Celery
from src.db import async_session_maker
from src.files.services.scan_file_for_threats import scan_file_for_threats
from src.files.services.extract_file_metadata import extract_file_metadata
from src.files.services.send_file_alert import send_file_alert
from src.types import Err

REDIS_URL = os.environ.get("REDIS_URL", "redis://backend-redis:6379/0")
celery_app = Celery("file_tasks", broker=REDIS_URL, backend=REDIS_URL)

_loop = asyncio.new_event_loop()
asyncio.set_event_loop(_loop)


def _run(coro):
    return _loop.run_until_complete(coro)


@celery_app.task
def process_scan_file_for_threats(file_id: uuid.UUID) -> None:
    async def _task():
        async with async_session_maker() as session:
            return await scan_file_for_threats(session, file_id)

    scan_result = _run(_task())
    if isinstance(scan_result, Err):
        print(scan_result.error)
        return

    process_extract_file_metadata.delay(file_id)


@celery_app.task
def process_extract_file_metadata(file_id: uuid.UUID) -> None:
    async def _task():
        async with async_session_maker() as session:
            return await extract_file_metadata(session, file_id)

    extract_result = _run(_task())
    if isinstance(extract_result, Err):
        print(extract_result.error)
        return

    process_send_file_alert.delay(file_id)


@celery_app.task
def process_send_file_alert(file_id: uuid.UUID) -> None:
    async def _task():
        async with async_session_maker() as session:
            return await send_file_alert(session, file_id)

    _run(_task())
