# Transcription Service

A Dockerized audio transcription service using **FastAPI**, **Celery**, **Redis**, **PostgreSQL**, and **OpenAI Whisper**.  
It accepts audio files, transcribes them asynchronously, and returns text with timestamps per segment.

---

## Features

- Upload audio files (WAV/MP3) for transcription
- Background processing with **Celery** and **Redis**
- Returns full text and segmented transcription with timestamps
- Handles long audio files asynchronously
- Supports concurrent uploads

---

## System Design & Engineering Decisions

1. **Audio Format Handling**
   - Supports common audio formats (WAV, MP3)
   - Converted internally to WAV 16kHz, mono for Whisper model compatibility
   - Ensures consistent sample rate and encoding for accurate transcription

2. **Long Audio Files**
   - Processed asynchronously via **Celery workers**
   - Files can be segmented internally to reduce memory usage and speed up transcription

3. **Concurrency**
   - Multiple uploads handled by Celery + Redis queue
   - API is non-blocking, returns a **task ID** immediately
   - Worker pool size can be configured for higher concurrency

4. **Storage**
   - Audio files stored in `/uploads` directory
   - Transcripts stored in **PostgreSQL**
   - File paths saved in DB to map tasks to files

5. **Retries & Failures**
   - Celery automatically retries failed tasks (configurable)
   - Failed transcriptions marked as `"failed"` in DB for monitoring

6. **API Exposure**
   - FastAPI exposes endpoints:
     - `POST /transcriptions` → upload audio and create task
     - `GET /transcriptions/{task_id}` → check status and fetch result
   - Supports Swagger UI (`http://localhost:8000/docs`) for testing

7. **Docker & Deployment**
   - Docker Compose orchestrates **API, Worker, Redis, PostgreSQL**
   - Containers ensure reproducible environment
   - Background worker separation ensures API remains responsive

---

## Getting Started

### Prerequisites

- Docker & Docker Compose installed
- Python 3.10+ (if running locally outside Docker)

### Run with Docker Compose

```bash
docker compose build --no-cache
docker compose up