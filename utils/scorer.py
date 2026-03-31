from utils.llm import call_llm

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

    import re
    import json
    try:
        json_match = re.search(r'\{.*\}', result, re.DOTALL)
        return json.loads(json_match.group())
    except Exception as e:
        print("❌ Failed to parse ATS score:", e)
        return None