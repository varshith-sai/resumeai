from utils.llm import call_llm
import json
import re


def _fallback_score(job_description, resume_text):
    # Lightweight deterministic fallback when LLM JSON parsing fails.
    jd = job_description.lower()
    resume = resume_text.lower()

    # Keep only technical-ish tokens (length >= 3, letters/numbers/+/#/.-).
    raw_tokens = re.findall(r"[a-zA-Z][a-zA-Z0-9+#.\-]{2,}", jd)
    stopwords = {
        "with", "that", "this", "from", "your", "have", "will", "role", "team",
        "work", "using", "years", "year", "good", "strong", "skills", "ability",
        "development", "developer", "experience", "environment", "project",
        "knowledge", "understanding", "responsibilities", "familiarity",
    }
    technical = sorted({t for t in raw_tokens if t not in stopwords})

    matched = [k for k in technical if k in resume]
    missing = [k for k in technical if k not in resume]

    # Scale score by technical keyword coverage.
    total = len(technical) or 1
    score = int(round((len(matched) / total) * 100))

    return {
        "ats_score": score,
        "matched_keywords": matched[:25],
        "missing_keywords": missing[:25],
        "strengths": [
            "Resume includes several technical keywords from the job description."
            if matched else "Resume can include more explicit technical keywords."
        ],
        "improvements": [
            "Add more job-specific technologies and tools in projects/experience bullets."
            if missing else "Good keyword alignment. Keep bullets concise and impact-driven."
        ],
    }

def score_resume(job_description, resume_data):
    # Convert resume data to plain text for scoring
    resume_text = f"""
Name: {resume_data['name']}
Summary: {resume_data['summary']}
Skills: {resume_data['skills']}
Experience: {resume_data['experience']}
Projects: {resume_data['projects']}
"""

    prompt = f"""
You are an ATS (Applicant Tracking System) expert.

Extract ONLY technical skills, tools, and technologies explicitly mentioned in the job description.
Ignore soft skills, phrases, and action verbs like "collaborate", "deploy", "develop", "analyze".
Focus only on: programming languages, libraries, frameworks, platforms, and technical concepts.
Check which of those exact technical keywords appear in the resume.
Do NOT invent keywords. Only flag a keyword as missing if it is a technical term explicitly in the job description.


JOB DESCRIPTION:
{job_description}

RESUME:
{resume_text}

Return ONLY valid JSON, no explanation, no markdown:
{{
  "ats_score": 90,
  "matched_keywords": ["keywords from JD that ARE in resume"],
  "missing_keywords": ["keywords from JD that are NOT in resume"],
  "strengths": ["strength 1", "strength 2"],
  "improvements": ["improvement 1", "improvement 2"]
}}
"""


    result = call_llm(prompt)

    try:
        json_match = re.search(r'\{.*\}', result, re.DOTALL)
        parsed = json.loads(json_match.group())
        # Guard against partially malformed model outputs.
        if not isinstance(parsed, dict):
            return _fallback_score(job_description, resume_text)
        parsed.setdefault("matched_keywords", [])
        parsed.setdefault("missing_keywords", [])
        parsed.setdefault("strengths", [])
        parsed.setdefault("improvements", [])
        parsed.setdefault("ats_score", 0)
        return parsed
    except Exception as e:
        print("❌ Failed to parse ATS score:", e)
        return _fallback_score(job_description, resume_text)