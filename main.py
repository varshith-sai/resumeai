# from utils.github import get_github_projects

# projects = get_github_projects()
# for p in projects:
#     print(f"📁 {p['name']} | {p['description']} | Languages: {p['languages']}")



import os
import re
import json
import subprocess
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from utils.llm import call_llm
from utils.github import get_github_projects

# ─────────────────────────────────────────
# 1. LOAD INPUTS
# ─────────────────────────────────────────
def load_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

job_description = """
Data Science Internship Summer 2026
- Develop machine learning models for predictive analytics
- Analyze large datasets and generate actionable insights
- Collaborate with engineering team to deploy ML solutions
Requirements: Python, SQL, scikit-learn, pandas, NumPy, statistics
"""

master_resume = load_file("data/master_resume.txt")

# Fetch GitHub projects
github_projects = get_github_projects()
github_text = "\n".join([
    f"- {p['name']}: {p['description']} (Languages: {', '.join(p['languages'])})"
    for p in github_projects
])

# ─────────────────────────────────────────
# 2. CALL LLM → GET JSON
# ─────────────────────────────────────────
prompt = f"""
You are a resume writer. Based on the job description and master resume, return ONLY a valid JSON object. No explanation, no markdown, no code blocks, just raw JSON.

JOB DESCRIPTION:
{job_description}

MASTER RESUME:
{master_resume}

GITHUB PROJECTS (pick the most relevant ones for the job):
{github_text}

Select 2-3 most relevant projects from above based on the job description.
For each selected project, write exactly 2 bullet points describing what was built and the impact.
Use the project name exactly as shown.
Keep summary to 1 sentence only.
Limit experience to maximum 2 bullet points.
Keep skills concise, only most relevant ones.
Limit awards to maximum 2.
IMPORTANT: Naturally include as many keywords from the job description as possible in bullets and summary.
Do NOT stuff keywords unnaturally — weave them in meaningfully.


Return this exact JSON structure:
{{
  "name": "Full Name",
  "phone": "+1 (567) 219-0292",
  "email": "vsai24723@gmail.com",
  "location": "Long Beach, CA",
  "linkedin": "https://www.linkedin.com/in/varshith-sai-manchem-684199257/",
  "github": "https://github.com/varshith-sai",
  "summary": "2-3 sentence professional summary tailored to job",
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
  "education": [
    {{
      "degree": "Master of Science in Information Systems",
      "school": "California State University, Long Beach",
      "dates": "Aug 2025 - May 2027"
    }},
    {{
      "degree": "Bachelor of Technology in Information Technology",
      "school": "Gokaraju Rangaraju Institute of Engineering and Technology, Hyderabad",
      "dates": "2021 - 2025",
      "gpa": "CGPA: 7.98/10"
    }}
  ]
}}
"""

print("⏳ Calling LLM...")
result = call_llm(prompt)

try:
    json_match = re.search(r'\{.*\}', result, re.DOTALL)
    data = json.loads(json_match.group())
    print("✅ JSON parsed successfully")
except Exception as e:
    print("❌ Failed to parse JSON:", e)
    print("Raw output:", result)
    exit()

# ─────────────────────────────────────────
# 3. BUILD DOCX MATCHING YOUR FORMAT
# ─────────────────────────────────────────
def build_resume(data):
    doc = Document()

    # Page margins (narrow like your resume)
    for section in doc.sections:
        section.top_margin = Inches(0.5)
        section.bottom_margin = Inches(0.5)
        section.left_margin = Inches(0.75)
        section.right_margin = Inches(0.75)

    def set_font(run, size, bold=False, color=None):
        run.font.name = "Calibri"
        run.font.size = Pt(size)
        run.font.bold = bold
        if color:
            run.font.color.rgb = RGBColor(*color)

    def add_section_header(doc, title):
        """Add ALL CAPS bold section header with bottom border line"""
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(6)
        p.paragraph_format.space_after = Pt(2)
        run = p.add_run(title.upper())
        set_font(run, 10, bold=True)
        # Add bottom border
        pPr = p._p.get_or_add_pPr()
        pBdr = OxmlElement('w:pBdr')
        bottom = OxmlElement('w:bottom')
        bottom.set(qn('w:val'), 'single')
        bottom.set(qn('w:sz'), '6')
        bottom.set(qn('w:space'), '1')
        bottom.set(qn('w:color'), '000000')
        pBdr.append(bottom)
        pPr.append(pBdr)
        return p

    def add_bullet(doc, text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.left_indent = Inches(0.25)
        run = p.add_run(f"\u2022  {text}")
        set_font(run, 10)
        return p

    # ── NAME ──
    name_p = doc.add_paragraph()
    name_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    name_p.paragraph_format.space_after = Pt(2)
    name_run = name_p.add_run(data['name'])
    set_font(name_run, 14, bold=True)

    # ── CONTACT INFO ──
    def add_hyperlink(paragraph, text, url):
        part = paragraph.part
        r_id = part.relate_to(url, 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink', is_external=True)
        hyperlink = OxmlElement('w:hyperlink')
        hyperlink.set(qn('r:id'), r_id)
        run = OxmlElement('w:r')
        rPr = OxmlElement('w:rPr')
        rStyle = OxmlElement('w:rStyle')
        rStyle.set(qn('w:val'), 'Hyperlink')
        rPr.append(rStyle)
        run.append(rPr)
        t = OxmlElement('w:t')
        t.text = text
        run.append(t)
        hyperlink.append(run)
        paragraph._p.append(hyperlink)

    contact_p = doc.add_paragraph()
    contact_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    contact_p.paragraph_format.space_after = Pt(4)

    # Plain text parts
    r1 = contact_p.add_run(f"{data['phone']} ǀ {data['email']} ǀ {data['location']} ǀ ")
    set_font(r1, 10)

    # Clickable LinkedIn
    add_hyperlink(contact_p, "LinkedIn", data['linkedin'])

    r2 = contact_p.add_run(" | ")
    set_font(r2, 10)

    # Clickable Github
    add_hyperlink(contact_p, "Github", data['github'])


    # ── PROFESSIONAL SUMMARY ──
    add_section_header(doc, "Professional Summary")
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(2)
    run = p.add_run(data['summary'])
    set_font(run, 10)

    # ── TECHNICAL SKILLS ──
    add_section_header(doc, "Technical Skills")
    for category, items in data['skills'].items():
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        bold_run = p.add_run(f"{category}: ")
        set_font(bold_run, 10, bold=True)
        normal_run = p.add_run(items)
        set_font(normal_run, 10)

    # ── WORK EXPERIENCE ──
    add_section_header(doc, "Work Experience")
    for exp in data['experience']:
        # Company + dates on same line
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(0)
        left_run = p.add_run(f"{exp['company']} | {exp['location']}")
        set_font(left_run, 10, bold=True)
        tab_run = p.add_run(f"  {exp['dates']}")
        set_font(tab_run, 10, bold=True)

        # Title
        p2 = doc.add_paragraph()
        p2.paragraph_format.space_before = Pt(0)
        p2.paragraph_format.space_after = Pt(0)
        title_run = p2.add_run(exp['title'])
        set_font(title_run, 10, bold=True)

        for bullet in exp['bullets']:
            add_bullet(doc, bullet)

    # ── ACADEMIC PROJECTS ──
    add_section_header(doc, "Academic Project")
    for proj in data['projects']:
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(0)
        proj_run = p.add_run(proj['name'])
        set_font(proj_run, 10, bold=True)
        for bullet in proj['bullets']:
            add_bullet(doc, bullet)

    # ── AWARDS & ACTIVITIES ──
    add_section_header(doc, "Awards & Activities")
    for award in data['awards']:
        add_bullet(doc, award)

    # ── EDUCATION ──
    add_section_header(doc, "Academic Qualification")
    for edu in data['education']:
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(0)
        degree_run = p.add_run(edu['degree'])
        set_font(degree_run, 10, bold=True)
        date_run = p.add_run(f"  {edu['dates']}")
        set_font(date_run, 10, bold=True)

        p2 = doc.add_paragraph()
        p2.paragraph_format.space_before = Pt(0)
        p2.paragraph_format.space_after = Pt(0)
        school_run = p2.add_run(edu['school'])
        set_font(school_run, 10)

        if 'gpa' in edu:
            gpa_run = p2.add_run(f"  {edu['gpa']}")
            set_font(gpa_run, 10)

    # ─────────────────────────────────────────
    # 4. SAVE
    # ─────────────────────────────────────────
    os.makedirs("output", exist_ok=True)
    output_path = "output/resume.docx"
    doc.save(output_path)
    return output_path

from docx2pdf import convert

# Call build_resume to generate the docx
output_path = build_resume(data)
print(f"✅ Resume saved: {output_path}")

# Convert to PDF
pdf_path = "output/resume.pdf"
convert(output_path, pdf_path)
print(f"✅ PDF saved: {pdf_path}")


# ─────────────────────────────────────────
# 5. ATS SCORING — FIRST PASS
# ─────────────────────────────────────────
from utils.scorer import score_resume

print("\n⏳ Scoring resume against job description...")
score = score_resume(job_description, data)
if score:
    print(f"\n{'='*50}")
    print(f"📊 ATS SCORE: {score['ats_score']}/100")
    print(f"✅ Matched: {', '.join(score['matched_keywords'])}")
    print(f"❌ Missing: {', '.join(score['missing_keywords'])}")
    print(f"{'='*50}\n")


# ─────────────────────────────────────────
# 6. KEYWORD INJECTION — SECOND PASS
# ─────────────────────────────────────────
if score and score['missing_keywords']:
    print(f"\n⏳ Injecting missing keywords and regenerating...")

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
        print("✅ Keywords injected successfully")

        # Rebuild and save docx + pdf with updated data
        # (re-run the docx generation with new data)
        # Rebuild resume with injected keywords
        output_path = build_resume(data)
        convert(output_path, pdf_path)
        print("✅ Updated PDF saved with injected keywords")

    except Exception as e:
        print("❌ Failed to inject keywords:", e)

    # Rescore
    print("\n⏳ Rescoring updated resume...")
    score2 = score_resume(job_description, data)
    if score2:
        print(f"\n{'='*50}")
        print(f"📊 UPDATED ATS SCORE: {score2['ats_score']}/100")
        print(f"✅ Matched: {', '.join(score2['matched_keywords'])}")
        print(f"❌ Still Missing: {', '.join(score2['missing_keywords'])}")
        print(f"{'='*50}\n")
