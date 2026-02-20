import whisper
import uuid
import ffmpeg
from app.database import SessionLocal
from app.models import Transcription

model = whisper.load_model("base")

def normalize_audio(input_path, output_path):
    (
        ffmpeg
        .input(input_path)
        .output(output_path,
                format="wav",
                acodec="pcm_s16le",
                ac=1,
                ar="16000")
        .run(overwrite_output=True)
    )

def process_transcription(job_id, file_path):
    db = SessionLocal()

    normalized = f"{file_path}_normalized.wav"
    normalize_audio(file_path, normalized)

    result = model.transcribe(normalized)

    segments = [
        {
            "start": s["start"],
            "end": s["end"],
            "text": s["text"].strip()
        }
        for s in result["segments"]
    ]

    job = db.query(Transcription).filter_by(id=job_id).first()
    job.status = "completed"
    job.full_text = result["text"]
    job.segments = segments
    db.commit()
    db.close()