import streamlit as st
import os
from utils.generator import generate_resume

st.set_page_config(
    page_title="ResumeAI",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── CUSTOM CSS ──
st.markdown("""
<style>
    /* Hide default streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Main background */
    .stApp {
        background-color: #1a1a2e;
        color: #e0e0e0;
    }

    /* Center container */
    .main-container {
        max-width: 800px;
        margin: 0 auto;
        padding: 2rem 1rem;
    }

    /* Logo/title area */
    .hero {
        text-align: center;
        padding: 3rem 0 2rem 0;
    }

    .hero h1 {
        font-size: 2.8rem;
        font-weight: 700;
        background: linear-gradient(135deg, #6c63ff, #3ecfcf);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }

    .hero p {
        color: #888;
        font-size: 1.1rem;
    }

    /* Job card */
    .job-card {
        background: #16213e;
        border: 1px solid #2a2a4a;
        border-radius: 12px;
        padding: 1.2rem;
        margin-bottom: 1rem;
    }

    /* Input fields */
    .stTextInput input, .stTextArea textarea {
        background-color: #0f3460 !important;
        color: #e0e0e0 !important;
        border: 1px solid #2a2a4a !important;
        border-radius: 8px !important;
    }

    /* Generate button */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #6c63ff, #3ecfcf) !important;
        color: white !important;
        border: none !important;
        border-radius: 25px !important;
        padding: 0.6rem 2.5rem !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        width: 100% !important;
        margin-top: 1rem !important;
    }

    /* Add job button */
    .stButton > button:not([kind="primary"]) {
        background: #16213e !important;
        color: #6c63ff !important;
        border: 1px solid #6c63ff !important;
        border-radius: 20px !important;
        padding: 0.3rem 1.2rem !important;
    }

    /* Result card */
    .result-card {
        background: #16213e;
        border: 1px solid #2a2a4a;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
    }

    .result-title {
        font-size: 1.2rem;
        font-weight: 600;
        color: #e0e0e0;
        margin-bottom: 1rem;
    }

    /* ATS score badge */
    .ats-badge-green {
        background: #1a472a;
        color: #4caf50;
        border-radius: 20px;
        padding: 0.3rem 1rem;
        font-weight: 700;
        font-size: 1rem;
        display: inline-block;
    }

    .ats-badge-orange {
        background: #3d2a00;
        color: #ff9800;
        border-radius: 20px;
        padding: 0.3rem 1rem;
        font-weight: 700;
        font-size: 1rem;
        display: inline-block;
    }

    .ats-badge-red {
        background: #3d0000;
        color: #f44336;
        border-radius: 20px;
        padding: 0.3rem 1rem;
        font-weight: 700;
        font-size: 1rem;
        display: inline-block;
    }

    /* Keyword tags */
    .keyword-matched {
        background: #1a472a;
        color: #4caf50;
        border-radius: 12px;
        padding: 0.2rem 0.6rem;
        font-size: 0.8rem;
        margin: 2px;
        display: inline-block;
    }

    .keyword-missing {
        background: #3d0000;
        color: #f44336;
        border-radius: 12px;
        padding: 0.2rem 0.6rem;
        font-size: 0.8rem;
        margin: 2px;
        display: inline-block;
    }

    /* Download buttons */
    .stDownloadButton > button {
        background: #0f3460 !important;
        color: #e0e0e0 !important;
        border: 1px solid #2a2a4a !important;
        border-radius: 8px !important;
        width: 100% !important;
    }

    .stDownloadButton > button:hover {
        background: #6c63ff !important;
        border-color: #6c63ff !important;
    }

    /* Spinner */
    .stSpinner > div {
        border-top-color: #6c63ff !important;
    }

    /* Divider */
    hr {
        border-color: #2a2a4a !important;
    }

    /* Label text */
    .stTextInput label, .stTextArea label {
        color: #888 !important;
    }
</style>
""", unsafe_allow_html=True)

# ── HERO SECTION ──
st.markdown("""
<div class="hero">
    <h1>✨ ResumeAI</h1>
    <p>Generate tailored resumes and cover letters for every job in seconds</p>
</div>
""", unsafe_allow_html=True)

# ── SESSION STATE ──
if "jd_list" not in st.session_state:
    st.session_state.jd_list = [{"name": "Job 1", "description": ""}]
if "results" not in st.session_state:
    st.session_state.results = []

# ── JOB INPUT SECTION ──
st.markdown("### 📋 Job Descriptions")

for i, jd in enumerate(st.session_state.jd_list):
    with st.container():
        st.markdown(f'<div class="job-card">', unsafe_allow_html=True)
        col1, col2 = st.columns([5, 1])
        with col1:
            st.session_state.jd_list[i]["name"] = st.text_input(
                "Job Title", value=jd["name"], key=f"name_{i}",
                placeholder="e.g. Data Science Intern at Google"
            )
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🗑️", key=f"remove_{i}", help="Remove this job"):
                st.session_state.jd_list.pop(i)
                st.rerun()

        st.session_state.jd_list[i]["description"] = st.text_area(
            "Paste Job Description",
            value=jd["description"],
            height=160,
            key=f"desc_{i}",
            placeholder="Paste the full job description here..."
        )
        st.markdown('</div>', unsafe_allow_html=True)

# ── ADD JOB BUTTON ──
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("➕ Add Another Job"):
        count = len(st.session_state.jd_list) + 1
        st.session_state.jd_list.append({"name": f"Job {count}", "description": ""})
        st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

# ── GENERATE BUTTON ──
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    generate_clicked = st.button("🚀 Generate Resumes", type="primary")

if generate_clicked:
    valid_jds = [jd for jd in st.session_state.jd_list if jd["description"].strip()]
    if not valid_jds:
        st.error("Please enter at least one job description.")
    else:
        st.session_state.results = []
        for jd in valid_jds:
            with st.spinner(f"Generating resume for **{jd['name']}**..."):
                result_tuple = generate_resume(jd["description"], jd["name"])
                if result_tuple is None:
                    pdf_path, docx_path, score, cover_letter_path, error = None, None, None, None, "❌ Generator failed."
                else:
                    pdf_path, docx_path, score, cover_letter_path, error = result_tuple

                st.session_state.results.append({
                    "name": jd["name"],
                    "pdf_path": pdf_path,
                    "docx_path": docx_path,
                    "cover_letter_path": cover_letter_path,
                    "score": score,
                    "error": error
                })

# ── RESULTS SECTION ──
if st.session_state.results:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 📄 Your Resumes")

    for result in st.session_state.results:
        st.markdown('<div class="result-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="result-title">📁 {result["name"]}</div>', unsafe_allow_html=True)

        if result["error"]:
            st.error(result["error"])
        else:
            score = result["score"]
            if score:
                ats = score["ats_score"]
                badge_class = "ats-badge-green" if ats >= 85 else "ats-badge-orange" if ats >= 70 else "ats-badge-red"
                st.markdown(f'<span class="{badge_class}">ATS Score: {ats}/100</span>', unsafe_allow_html=True)
                st.markdown("<br><br>", unsafe_allow_html=True)

                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**✅ Matched Keywords**")
                    matched_html = " ".join([f'<span class="keyword-matched">{k}</span>' for k in score["matched_keywords"]])
                    st.markdown(matched_html, unsafe_allow_html=True)
                with col2:
                    st.markdown("**❌ Missing Keywords**")
                    missing = score["missing_keywords"]
                    if missing:
                        missing_html = " ".join([f'<span class="keyword-missing">{k}</span>' for k in missing])
                        st.markdown(missing_html, unsafe_allow_html=True)
                    else:
                        st.markdown('<span class="keyword-matched">None 🎉</span>', unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                if result["pdf_path"] and os.path.exists(result["pdf_path"]):
                    with open(result["pdf_path"], "rb") as f:
                        st.download_button(
                            label="⬇️ Download Resume PDF",
                            data=f,
                            file_name=os.path.basename(result["pdf_path"]),
                            mime="application/pdf",
                            key=f"pdf_{result['name']}"
                        )
            with col2:
                if result.get("cover_letter_path") and os.path.exists(result["cover_letter_path"]):
                    with open(result["cover_letter_path"], "rb") as f:
                        st.download_button(
                            label="⬇️ Download Cover Letter",
                            data=f,
                            file_name=os.path.basename(result["cover_letter_path"]),
                            mime="application/pdf",
                            key=f"cl_{result['name']}"
                        )

        st.markdown('</div>', unsafe_allow_html=True)
