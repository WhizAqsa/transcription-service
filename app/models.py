from sqlalchemy import Column, String, Text, JSON
from app.database import Base

class Transcription(Base):
    __tablename__ = "transcriptions"

    id = Column(String, primary_key=True)
    status = Column(String)
    file_path = Column(String)
    full_text = Column(Text, nullable=True)
    segments = Column(JSON, nullable=True)