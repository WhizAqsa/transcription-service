from celery import Celery
from app.transcription import process_transcription

celery = Celery(
    "worker",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0"
)

@celery.task(bind=True, max_retries=3)
def transcribe_task(self, job_id, file_path):
    try:
        process_transcription(job_id, file_path)
    except Exception as e:
        raise self.retry(exc=e, countdown=5)