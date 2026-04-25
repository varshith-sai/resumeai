import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi import FastAPI, UploadFile, File, Form, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from typing import List, Optional
import json
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address
from utils.generator import generate_resume
from utils.config import reload_config

app = FastAPI()

MAX_UPLOAD_BYTES = int(os.environ.get("MAX_UPLOAD_BYTES", str(25 * 1024 * 1024)))
_cors_raw = os.environ.get("CORS_ORIGINS", "").strip()
if _cors_raw:
    _allow_origins = [o.strip() for o in _cors_raw.split(",") if o.strip()]
else:
    _allow_origins = ["*"]

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=_allow_origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

class JobRequest(BaseModel):
    name: str
    description: str

class BatchRequest(BaseModel):
    jobs: List[JobRequest]
    hf_token: Optional[str] = None
    github_token: Optional[str] = None

@app.get("/")
def root():
    return {"status": "ResumeAI API running"}

def _safe_output_download_path(requested_path):
    if not requested_path or ".." in requested_path.replace("\\", "/"):
        return None
    output_root = os.path.abspath("output")
    full_path = os.path.abspath(requested_path)
    if not full_path.lower().endswith(".pdf"):
        return None
    if not full_path.startswith(output_root + os.sep):
        return None
    return full_path

@app.post("/setup")
@limiter.limit("8/minute")
async def setup(
    request: Request,
    personal: str = Form(...),
    education: str = Form(...),
    hf_token: str = Form(""),
    github_token: str = Form(""),
    master_resume_text: str = Form(""),
    master_resume_file: Optional[UploadFile] = File(None),
    linkedin_file: Optional[UploadFile] = File(None),
    resume_template_file: Optional[UploadFile] = File(None),
):
    content_length = request.headers.get("content-length")
    if content_length:
        try:
            if int(content_length) > MAX_UPLOAD_BYTES:
                raise HTTPException(status_code=413, detail="Request body too large")
        except ValueError:
            pass

    personal_data = json.loads(personal)
    education_data = json.loads(education)

    # Save config.yaml
    import yaml
    config = {
        "personal": personal_data,
        "education": education_data
    }
    with open("config.yaml", "w", encoding="utf-8") as f:
        yaml.dump(config, f)
    print("✅ config.yaml saved")

    # Save master resume
    os.makedirs("data", exist_ok=True)
    if master_resume_text.strip():
        with open("data/master_resume.txt", "w", encoding="utf-8") as f:
            f.write(master_resume_text)
        print("✅ master_resume.txt saved from text")
    elif master_resume_file:
        contents = await master_resume_file.read()
        if len(contents) > MAX_UPLOAD_BYTES:
            raise HTTPException(status_code=413, detail="Resume file too large")
        with open("data/master_resume.txt", "wb") as f:
            f.write(contents)
        print("✅ master_resume.txt saved from file")

    # Save resume template DOCX (user's own resume for style matching)
    if resume_template_file:
        contents = await resume_template_file.read()
        if len(contents) > MAX_UPLOAD_BYTES:
            raise HTTPException(status_code=413, detail="Template file too large")
        with open("data/resume_template.docx", "wb") as f:
            f.write(contents)
        print("✅ resume_template.docx saved — styles will be extracted from this")

    # Save LinkedIn PDF and run parser
    if linkedin_file:
        contents = await linkedin_file.read()
        if len(contents) > MAX_UPLOAD_BYTES:
            raise HTTPException(status_code=413, detail="LinkedIn PDF too large")
        with open("data/linkedin_profile.pdf", "wb") as f:
            f.write(contents)
        print("✅ linkedin_profile.pdf saved")
        try:
            from utils.linkedin_parser import run_linkedin_import
            run_linkedin_import()
            print("✅ LinkedIn data imported")
        except Exception as e:
            print(f"⚠️ LinkedIn import failed: {e}")

    # Update env tokens so generator uses them immediately
    if hf_token:
        os.environ["HF_API_TOKEN"] = hf_token
    if github_token:
        os.environ["GITHUB_TOKEN"] = github_token

    reload_config()
    return {"status": "Setup complete"}

@app.post("/generate")
@limiter.limit("15/minute")
def generate(request: Request, payload: BatchRequest):
    if payload.hf_token:
        os.environ["HF_API_TOKEN"] = payload.hf_token
    if payload.github_token:
        os.environ["GITHUB_TOKEN"] = payload.github_token

    results = []
    for job in payload.jobs:
        pdf_path, docx_path, score, cover_letter_path, error = generate_resume(
            job.description, job.name
        )
        results.append({
            "name": job.name,
            "pdf_path": pdf_path,
            "cover_letter_path": cover_letter_path,
            "score": score,
            "error": error
        })
    return {"results": results}

@app.get("/download")
@limiter.limit("60/minute")
def download(request: Request, path: str):
    safe_path = _safe_output_download_path(path)
    if not safe_path or not os.path.exists(safe_path):
        return JSONResponse({"error": "File not found"}, status_code=404)
    return FileResponse(
        safe_path,
        media_type="application/pdf",
        filename=os.path.basename(safe_path)
    )