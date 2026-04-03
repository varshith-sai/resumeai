import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional
import json
from utils.generator import generate_resume

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

@app.post("/setup")
async def setup(
    personal: str = Form(...),
    education: str = Form(...),
    hf_token: str = Form(""),
    github_token: str = Form(""),
    master_resume_text: str = Form(""),
    master_resume_file: Optional[UploadFile] = File(None),
    linkedin_file: Optional[UploadFile] = File(None),
    resume_template_file: Optional[UploadFile] = File(None),
):
    personal_data = json.loads(personal)
    education_data = json.loads(education)

    # Save config.yaml
    import yaml
    config = {
        "personal": personal_data,
        "education": education_data
    }
    with open("config.yaml", "w") as f:
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
        with open("data/master_resume.txt", "wb") as f:
            f.write(contents)
        print("✅ master_resume.txt saved from file")

    # Save resume template DOCX (user's own resume for style matching)
    if resume_template_file:
        contents = await resume_template_file.read()
        with open("data/resume_template.docx", "wb") as f:
            f.write(contents)
        print("✅ resume_template.docx saved — styles will be extracted from this")

    # Save LinkedIn PDF and run parser
    if linkedin_file:
        contents = await linkedin_file.read()
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

    return {"status": "Setup complete"}

@app.post("/generate")
def generate(request: BatchRequest):
    if request.hf_token:
        os.environ["HF_API_TOKEN"] = request.hf_token
    if request.github_token:
        os.environ["GITHUB_TOKEN"] = request.github_token

    results = []
    for job in request.jobs:
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
def download(path: str):
    if not os.path.exists(path):
        return {"error": "File not found"}
    return FileResponse(
        path,
        media_type="application/pdf",
        filename=os.path.basename(path)
    )