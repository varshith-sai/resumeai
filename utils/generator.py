import os
import re
import json
from utils.llm import call_llm
from utils.github import get_github_projects
from utils.scorer import score_resume
from utils.resume_builder import build_resume
from utils.cover_letter import generate_cover_letter
from utils.config import personal, education


def load_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


# Load master resume and GitHub projects once
try:
    master_resume = load_file("data/master_resume.txt")
    print("✅ master_resume loaded")
except Exception as e:
    print(f"❌ Could not load master_resume.txt: {e}")
    master_resume = ""

try:
    github_projects = get_github_projects()
    github_text = "\n".join([
        f"- {p['name']}: {p['description']} (Languages: {', '.join(p['languages'])})"
        for p in github_projects
    ])
    print("✅ GitHub projects loaded")
except Exception as e:
    print(f"❌ Could not fetch GitHub projects: {e}")
    github_text = ""


def select_relevant_projects(github_projects, job_description):
    """Match projects to JD based on keyword overlap"""
    jd_lower = job_description.lower()

    scored = []
    for p in github_projects:
        score = 0
        text = (p['name'] + " " + p['description'] + " " + " ".join(p['languages'])).lower()

        keywords = jd_lower.split()
        for word in keywords:
            if len(word) > 4 and word in text:
                score += 1

        for lang in p['languages']:
            if lang.lower() in jd_lower:
                score += 3

        scored.append((score, p))

    scored.sort(key=lambda x: x[0], reverse=True)
    top3 = [p for _, p in scored[:3]]

    return "\n".join([
        f"- {p['name']}: {p['description']} (Languages: {', '.join(p['languages'])})"
        for p in top3
    ])


def generate_resume(job_description, job_name="job"):
    """
    Full pipeline: JD → JSON → DOCX → PDF → ATS score → Cover Letter
    Returns: (pdf_path, docx_path, score, cover_letter_path, error)
    """
    try:
        # ── STEP 1: Generate resume JSON from LLM ──
        import json as _json
        education_json = _json.dumps(education, indent=2)
        prompt = f"""
You are a resume writer. Based on the job description and master resume, return ONLY a valid JSON object. No explanation, no markdown, no code blocks, just raw JSON.

JOB DESCRIPTION:
{job_description}

MASTER RESUME:
{master_resume}

GITHUB PROJECTS (use ONLY these projects, do not pick others):
{select_relevant_projects(github_projects, job_description)}

Carefully read the job description and select 3 projects from the GITHUB PROJECTS list that are MOST RELEVANT to this specific job.
Different job descriptions must result in different project selections.
Match projects based on: programming languages used, technologies mentioned, and domain (ML, web, data, NLP, etc).
For each selected project, write exactly 2 bullet points describing what was built and the impact.
Use the project name exactly as shown from the GITHUB PROJECTS list.
Do NOT always pick the same projects — pick based on what the job actually requires.

Keep summary to 1 sentence only.
Limit experience to maximum 2 bullet points.
Keep skills concise, only most relevant ones.
Limit awards to maximum 2.
IMPORTANT: Naturally include as many keywords from the job description as possible in bullets and summary.
Do NOT stuff keywords unnaturally — weave them in meaningfully.
STRICT ONE PAGE RULES — CRITICAL, DO NOT IGNORE:
- Summary: exactly 1 sentence, maximum 15 words
- Experience: exactly 2 bullet points, each maximum 15 words
- Projects: exactly 3 projects, exactly 2 bullet points each, each maximum 15 words
- Skills: maximum 3 items per category
- Awards: exactly 2 only
- Every bullet point must be concise — no long sentences

Return this exact JSON structure:
{{
  "name": "{personal['name']}",
  "phone": "{personal['phone']}",
  "email": "{personal['email']}",
  "location": "{personal['location']}",
  "linkedin": "{personal['linkedin']}",
  "github": "{personal['github']}",
  "summary": "1 sentence professional summary tailored to job",
  "skills": {{
    "Programming Languages": "Java, Python",
    "Database Management": "SQL, Data Warehousing",
    "Software Tools": "Power BI, IBM SPSS",
    "Methodologies": "Google Advanced Data Analytics",
    "Concepts": "AWS Cloud Services, Machine Learning"
  }},
  "experience": [
    {{
      "company": "Company Name",
      "location": "City, Country",
      "title": "Internship",
      "dates": "Aug 2024 - Jan 2025",
      "bullets": [
        "Achievement 1 with metric",
        "Achievement 2 with metric"
      ]
    }}
  ],
  "projects": [
    {{
      "name": "Project Name",
      "bullets": [
        "Description point 1",
        "Description point 2"
      ]
    }}
  ],
  "awards": [
    "Award 1",
    "Award 2"
  ],
  "education": {education_json}
}}
"""

        result = call_llm(prompt)

        try:
            json_match = re.search(r'\{.*\}', result, re.DOTALL)
            data = json.loads(json_match.group())
        except Exception as e:
            return None, None, None, None, f"❌ Failed to parse JSON: {e}"

        # ── STEP 2: ATS Score first pass ──
        score = score_resume(job_description, data)

        # ── STEP 3: Keyword injection if needed ──
        if score and score['missing_keywords']:
            missing = ', '.join(score['missing_keywords'])
            inject_prompt = f"""
You are a resume writer. You have a resume in JSON format.
Rewrite ONLY the summary, skills, experience bullets, and project bullets
to naturally include these missing keywords: {missing}

Do NOT change name, email, phone, location, linkedin, github, education, awards.
Do NOT stuff keywords unnaturally — weave them in meaningfully.
Return ONLY valid JSON with the same structure, no explanation, no markdown.

CURRENT RESUME JSON:
{json.dumps(data)}

JOB DESCRIPTION:
{job_description}
"""
            result2 = call_llm(inject_prompt)
            try:
                json_match2 = re.search(r'\{.*\}', result2, re.DOTALL)
                data = json.loads(json_match2.group())
                score = score_resume(job_description, data)
            except Exception:
                pass

        # ── STEP 4: Build DOCX + PDF ──
        os.makedirs("output", exist_ok=True)
        safe_name = job_name.replace(" ", "_").replace("/", "_")
        docx_path = f"output/{safe_name}.docx"
        pdf_path = f"output/{safe_name}.pdf"

        template_path = "data/resume_template.docx"
        if os.path.exists(template_path):
            from utils.template_parser import build_resume_from_template
            build_resume_from_template(data, docx_path, template_path)
        else:
            build_resume(data, docx_path)

        import subprocess
        import platform

        if platform.system() == "Windows":
            import pythoncom
            from docx2pdf import convert as docx_convert
            pythoncom.CoInitialize()
            try:
                docx_convert(docx_path, pdf_path)
            finally:
                pythoncom.CoUninitialize()
        else:
            # Linux (for deployment)
            subprocess.run([
                "libreoffice", "--headless", "--convert-to", "pdf",
                "--outdir", os.path.dirname(pdf_path), docx_path
            ], check=True)

        # ── STEP 5: Generate Cover Letter ──
        cover_letter_path = generate_cover_letter(job_description, job_name)

        return pdf_path, docx_path, score, cover_letter_path, None

    except Exception as e:
        print(f"❌ generate_resume crashed: {e}")
        import traceback
        traceback.print_exc()
        return None, None, None, None, f"❌ Error: {e}"
