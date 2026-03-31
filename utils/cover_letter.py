import os
from fpdf import FPDF
from utils.llm import call_llm
from datetime import date
from utils.config import personal


def generate_cover_letter(job_description, job_name="job", master_resume_path="data/master_resume.txt"):
    try:
        with open(master_resume_path, "r", encoding="utf-8") as f:
            master_resume = f.read()

        prompt = f"""
You are a professional cover letter writer.

Write a tailored cover letter based on the job description and resume below.

JOB DESCRIPTION:
{job_description}

RESUME:
{master_resume}

RULES:
- Do NOT include any header, name, address, or date — just the letter body
- Start directly with: Dear Hiring Manager,
- Write exactly 3 short paragraphs:
  Paragraph 1: Who you are, what role you want, why excited (2-3 sentences)
  Paragraph 2: 2 specific skills or projects that match this job (2-3 sentences)
  Paragraph 3: Call to action and thank you (1-2 sentences)
- End with exactly: Sincerely, [blank line] {personal['name']}
- Maximum 180 words total
- No bullet points, no special characters, plain text only
- Output ONLY the letter body, nothing else
"""

        result = call_llm(prompt)
        print(f"📝 Cover letter LLM result: {result[:200] if result else 'None'}")
        if not result:
            print("❌ LLM returned None for cover letter")
            return None

        cover_letter_text = result.strip()
        cover_letter_text = cover_letter_text.encode("latin-1", errors="replace").decode("latin-1")

        # ── BUILD PDF ──
        os.makedirs("output", exist_ok=True)
        safe_name = job_name.replace(" ", "_").replace("/", "_")
        pdf_path = f"output/{safe_name}_cover_letter.pdf"

        pdf = FPDF()
        pdf.add_page()
        pdf.set_margins(25, 25, 25)
        pdf.set_auto_page_break(auto=True, margin=25)
        w = pdf.w - 50  # effective width

        # ── SENDER INFO ──
        pdf.set_font("Helvetica", "B", 13)
        pdf.cell(w, 8, personal['name'], ln=True)
        pdf.set_font("Helvetica", "", 10)
        pdf.cell(w, 6, f"{personal['location']}  |  {personal['phone']}  |  {personal['email']}", ln=True)
        pdf.cell(w, 6, f"{personal['linkedin']}  |  {personal['github']}", ln=True)

        # ── DIVIDER LINE ──
        pdf.set_draw_color(0, 0, 0)
        pdf.set_line_width(0.3)
        pdf.line(25, pdf.get_y(), pdf.w - 25, pdf.get_y())
        pdf.ln(6)

        # ── DATE ──
        pdf.set_font("Helvetica", "", 10)
        pdf.cell(w, 6, date.today().strftime("%B %d, %Y"), ln=True)
        pdf.ln(4)

        # ── RECIPIENT ──
        pdf.set_font("Helvetica", "", 10)
        pdf.cell(w, 6, "Hiring Manager", ln=True)
        pdf.cell(w, 6, job_name, ln=True)
        pdf.ln(6)

        # ── BODY ──
        pdf.set_font("Helvetica", "", 10)
        for line in cover_letter_text.split("\n"):
            line = line.strip()
            if line == "":
                pdf.ln(4)
            elif line.lower().startswith("sincerely"):
                pdf.ln(4)
                pdf.multi_cell(w, 6, "Sincerely,", align="L")
                pdf.ln(6)
                pdf.set_font("Helvetica", "B", 10)
                pdf.multi_cell(w, 6, personal['name'], align="L")
                pdf.set_font("Helvetica", "", 10)
                break
            else:
                pdf.multi_cell(w, 6, line, align="L")

        pdf.output(pdf_path)
        return pdf_path

    except Exception as e:
        print(f"❌ Cover letter generation failed: {e}")
        import traceback
        traceback.print_exc()
        return None
