import re
import json
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pypdf import PdfReader
from utils.llm import call_llm



def extract_linkedin_pdf(pdf_path="data/linkedin_profile.pdf"):
    """Extract raw text from LinkedIn PDF"""
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text


def parse_linkedin_with_llm(raw_text):
    """Use LLM to extract structured data from LinkedIn PDF text"""
    prompt = f"""
Extract information from this LinkedIn profile text and return ONLY valid JSON, no explanation, no markdown.

LINKEDIN PROFILE TEXT:
{raw_text[:4000]}

Return this exact JSON structure:
{{
  "certifications": [
    "Certification Name - Issuing Organization - Year"
  ],
  "courses": [
    "Course Name - Platform/Organization"
  ],
  "honors": [
    "Honor or Award Name - Organization - Year"
  ],
  "volunteer": [
    "Role - Organization - Description"
  ],
  "languages": [
    "Language - Proficiency Level"
  ],
  "about": "Summary text from About section"
}}

If a section is not found, return an empty list [] for it.
"""
    result = call_llm(prompt)
    try:
        json_match = re.search(r'\{.*\}', result, re.DOTALL)
        return json.loads(json_match.group())
    except Exception as e:
        print(f"❌ Failed to parse LinkedIn data: {e}")
        return None


def update_master_resume(linkedin_data, master_resume_path="data/master_resume.txt"):
    """Append LinkedIn data to master_resume.txt"""
    if not linkedin_data:
        return

    additions = "\n\nLINKEDIN DATA:\n"

    if linkedin_data.get("certifications"):
        additions += "\nCERTIFICATIONS:\n"
        for c in linkedin_data["certifications"]:
            additions += f"- {c}\n"

    if linkedin_data.get("courses"):
        additions += "\nCOURSES:\n"
        for c in linkedin_data["courses"]:
            additions += f"- {c}\n"

    if linkedin_data.get("honors"):
        additions += "\nHONORS & AWARDS:\n"
        for h in linkedin_data["honors"]:
            additions += f"- {h}\n"

    if linkedin_data.get("volunteer"):
        additions += "\nVOLUNTEER EXPERIENCE:\n"
        for v in linkedin_data["volunteer"]:
            additions += f"- {v}\n"

    if linkedin_data.get("languages"):
        additions += "\nLANGUAGES:\n"
        for l in linkedin_data["languages"]:
            additions += f"- {l}\n"

    if linkedin_data.get("about"):
        additions += f"\nABOUT:\n{linkedin_data['about']}\n"

    # Append to master resume
    with open(master_resume_path, "a", encoding="utf-8") as f:
        f.write(additions)

    print("✅ LinkedIn data added to master_resume.txt")
    return additions


def run_linkedin_import():
    pdf_path = "data/linkedin_profile.pdf"

    if not os.path.exists(pdf_path):
        print("❌ linkedin_profile.pdf not found in data/ folder")
        return

    print("⏳ Reading LinkedIn PDF...")
    raw_text = extract_linkedin_pdf(pdf_path)

    print("⏳ Parsing with LLM...")
    linkedin_data = parse_linkedin_with_llm(raw_text)

    if linkedin_data:
        print("\n📋 Found:")
        print(f"  Certifications: {len(linkedin_data.get('certifications', []))}")
        print(f"  Courses: {len(linkedin_data.get('courses', []))}")
        print(f"  Honors: {len(linkedin_data.get('honors', []))}")
        update_master_resume(linkedin_data)
    else:
        print("❌ Could not parse LinkedIn data")


if __name__ == "__main__":
    run_linkedin_import()
# ```

# Now run this once to import your LinkedIn data:
# ```
# python utils/linkedin_parser.py