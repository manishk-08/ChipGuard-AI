from celery import Celery

from app.config import settings

celery_app = Celery(
    "chipguard",
    broker=settings.redis_url,
    backend=settings.redis_url,
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

celery_app.conf.task_routes = {
    "app.tasks.bom_tasks.*": {"queue": "bom_processing"},
    "app.tasks.compliance_tasks.*": {"queue": "compliance"},
}
