import uuid
import os
from fastapi import FastAPI, UploadFile, File
from app.database import Base, engine, SessionLocal
from app.models import Transcription
from app.worker import transcribe_task

Base.metadata.create_all(bind=engine)

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.post("/transcriptions")
async def create_transcription(file: UploadFile = File(...)):
    job_id = str(uuid.uuid4())
    file_path = os.path.join(UPLOAD_DIR, f"{job_id}_{file.filename}")

    with open(file_path, "wb") as f:
        f.write(await file.read())

    db = SessionLocal()
    db_job = Transcription(
        id=job_id,
        status="processing",
        file_path=file_path
    )
    db.add(db_job)
    db.commit()
    db.close()

    transcribe_task.delay(job_id, file_path)

    return {"job_id": job_id, "status": "processing"}


@app.get("/transcriptions/{job_id}")
def get_status(job_id: str):
    db = SessionLocal()
    job = db.query(Transcription).filter_by(id=job_id).first()
    db.close()
    return job


@app.get("/transcriptions/{job_id}/result")
def get_result(job_id: str):
    db = SessionLocal()
    job = db.query(Transcription).filter_by(id=job_id).first()
    db.close()

    if job.status != "completed":
        return {"status": job.status}

    return {
        "full_text": job.full_text,
        "segments": job.segments
    }