# ✨ ResumeAI — AI-Powered Resume & Cover Letter Generator

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi)
![React](https://img.shields.io/badge/React-Frontend-61dafb?style=for-the-badge&logo=react)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**Paste a job description → Get a tailored resume + cover letter in seconds**

[🐛 Report Bug](https://github.com/varshith-sai/resumeai/issues) · [💡 Request Feature](https://github.com/varshith-sai/resumeai/issues) · [🤝 Contribute](#contributing)

</div>

---

## 🎯 What is ResumeAI?

ResumeAI is a free, open-source tool that uses AI to generate **tailored resumes and cover letters** for every job you apply to — automatically.

- 🤖 AI tailors your resume to match each job description
- 📊 ATS scoring with matched vs missing keywords
- 🐙 Auto-pulls your GitHub projects and selects the most relevant ones
- 💼 Imports certifications from your LinkedIn PDF
- 📄 Exports Resume PDF + Cover Letter PDF instantly
- 🎨 Matches your own resume's exact fonts, colors and layout
- ✨ Beautiful animated UI built with React + Framer Motion

---

## 📋 Prerequisites

Make sure ALL of these are installed before starting:

| Tool | Version | Download |
|------|---------|----------|
| Python | 3.10+ | https://www.python.org/downloads/ |
| Node.js | 18+ | https://nodejs.org/ |
| Git | Any | https://git-scm.com/ |
| LibreOffice *(Mac/Linux only)* | Any | https://www.libreoffice.org/download/download-libreoffice/ |
| Microsoft Word *(Windows only)* | Any | Pre-installed on most Windows PCs |

> ⚠️ **Mac users**: LibreOffice is REQUIRED for PDF conversion. Install it before running anything.

> ⚠️ **Windows users**: Microsoft Word must be installed. Most Windows PCs already have it.

---

## 🔑 API Keys You Need (Both Free)

### 1. HuggingFace Token — for AI generation
1. Create a free account at https://huggingface.co/join
2. Go to https://huggingface.co/settings/tokens
3. Click **"New token"** → give it a name → set type to **"Fine-grained"**
4. Under **Permissions**, enable **"Make calls to Inference Providers"**
5. Click **"Create token"** → copy it

### 2. GitHub Token — to fetch your projects automatically
1. Go to https://github.com/settings/tokens
2. Click **"Generate new token (classic)"**
3. Give it a name → check **"public_repo"** scope
4. Click **"Generate token"** → copy it

---

## ⚡ Setup on Mac

### Step 1 — Clone the repo
```bash
git clone https://github.com/varshith-sai/resumeai.git
cd resumeai
```

### Step 2 — Install LibreOffice
Download from: https://www.libreoffice.org/download/download-libreoffice/

Install it like a normal Mac app, then add it to your PATH:
```bash
echo 'export PATH="/Applications/LibreOffice.app/Contents/MacOS:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

Verify it works:
```bash
soffice --version
```

### Step 3 — Create Python virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

> 💡 Run `source venv/bin/activate` every time you open a new terminal.

### Step 4 — Install all Python libraries
```bash
pip install --upgrade pip
pip install -r requirements-mac.txt
```

This installs every library the project uses:
- `fastapi` — backend API framework
- `uvicorn[standard]` — runs the FastAPI server
- `python-multipart` — handles file uploads in FastAPI
- `python-docx` — creates and reads DOCX files
- `fpdf2` — generates cover letter PDFs
- `openai` — connects to HuggingFace LLM API
- `requests` — makes HTTP requests to GitHub API
- `python-dotenv` — reads your `.env` file
- `pyyaml` — reads your `config.yaml` file
- `pypdf` — reads LinkedIn PDF files
- `streamlit` — legacy UI (kept for reference)

### Step 5 — Install frontend libraries
```bash
cd frontend
npm install
cd ..
```

This installs:
- `react` + `react-dom` — UI framework
- `axios` — HTTP requests to backend
- `framer-motion` — animations
- `lucide-react` — icons
- `tailwindcss` — styling
- `vite` — frontend build tool

### Step 6 — Set up config files
```bash
cp config.example.yaml config.yaml
cp .env.example .env
```

### Step 7 — Add your API tokens
Open `.env` in any text editor and fill in:
```
HF_API_TOKEN=paste_your_huggingface_token_here
GITHUB_TOKEN=paste_your_github_token_here
```

### Step 8 — Add your personal details
Open `config.yaml` and fill in your info:
```yaml
personal:
  name: "Your Full Name"
  phone: "+1 (000) 000-0000"
  email: "your@email.com"
  location: "City, State"
  linkedin: "https://www.linkedin.com/in/your-profile/"
  github: "https://github.com/your-username"
  github_username: "your-username"

education:
  - degree: "Master of Science in Computer Science"
    school: "Your University"
    dates: "Aug 2024 - May 2026"
  - degree: "Bachelor of Technology"
    school: "Your University"
    dates: "2020 - 2024"
    gpa: "GPA: 3.8/4.0"
```

### Step 9 — Add your master resume
Create the file `data/master_resume.txt` and paste your full resume in plain text:
```
NAME: Your Name

EXPERIENCE:
- Software Engineer at Company, Jan 2024 - Present
  - Built X which improved Y by Z%
  - Led team of N engineers

SKILLS:
Python, SQL, Machine Learning, AWS, React

AWARDS:
- Best Project Award - University 2024
```

### Step 10 — Run the app

Open **two separate terminal windows**:

**Terminal 1 — Backend:**
```bash
source venv/bin/activate
uvicorn backend.main:app --reload
```
You should see: `Uvicorn running on http://127.0.0.1:8000`

**Terminal 2 — Frontend:**
```bash
cd frontend
npm run dev
```
You should see: `Local: http://localhost:5173`

### Step 11 — Open in browser
Go to: **http://localhost:5173**

Complete the setup wizard on first visit — it will ask for your details, tokens, and resume.

---

## ⚡ Setup on Windows

### Step 1 — Clone the repo
```
git clone https://github.com/varshith-sai/resumeai.git
cd resumeai
```

### Step 2 — Create Python virtual environment
```
python -m venv venv
venv\Scripts\activate
```

> 💡 Run `venv\Scripts\activate` every time you open a new terminal.

### Step 3 — Install all Python libraries
```
pip install --upgrade pip
pip install -r requirements.txt
```

This installs everything in `requirements-mac.txt` PLUS:
- `docx2pdf` — converts DOCX to PDF using Microsoft Word
- `pywin32` — Windows COM interface (required for DOCX to PDF)

### Step 4 — Install frontend libraries
```
cd frontend
npm install
cd ..
```

### Step 5 — Set up config files
```
copy config.example.yaml config.yaml
copy .env.example .env
```

### Step 6 — Add your API tokens
Open `.env` in Notepad:
```
HF_API_TOKEN=paste_your_huggingface_token_here
GITHUB_TOKEN=paste_your_github_token_here
```

### Step 7 — Add your personal details
Open `config.yaml` in Notepad and fill in your info (same format as Mac Step 8).

### Step 8 — Add your master resume
Create `data\master_resume.txt` and paste your resume content.

### Step 9 — Run the app

Open **two separate terminals**:

**Terminal 1 — Backend:**
```
venv\Scripts\activate
uvicorn backend.main:app --reload
```

**Terminal 2 — Frontend:**
```
cd frontend
npm run dev
```

Open browser at: **http://localhost:5173**

---

## 🎮 How to Use

1. Open **http://localhost:5173**
2. Complete the **4-step setup wizard** (first visit only):
   - **Step 1** — Enter your name, email, phone, location, LinkedIn, GitHub
   - **Step 2** — Add your education details
   - **Step 3** — Paste your HuggingFace and GitHub tokens
   - **Step 4** — Paste your master resume text + optionally upload your existing DOCX resume (for style matching) + optionally upload LinkedIn PDF (for certifications)
3. On the main page, paste one or more **job descriptions**
4. Click **"Generate Resumes"**
5. Download **Resume PDF** and **Cover Letter PDF** for each job

---

## 🗂️ Project Structure

```
resumeai/
├── backend/
│   └── main.py                  # FastAPI: /setup /generate /download
├── frontend/
│   └── src/
│       ├── App.jsx              # Main app
│       └── components/
│           ├── Setup.jsx        # 4-step onboarding wizard
│           ├── Hero.jsx         # Animated header
│           ├── JobCard.jsx      # Job description input
│           ├── ResultCard.jsx   # Results with ATS score + downloads
│           ├── Loader.jsx       # Loading animation
│           └── Settings.jsx     # Update tokens anytime
├── utils/
│   ├── llm.py                   # HuggingFace LLM calls
│   ├── github.py                # Fetches GitHub projects
│   ├── scorer.py                # ATS keyword scoring
│   ├── generator.py             # Main pipeline: JD → resume → PDF → score
│   ├── resume_builder.py        # Builds DOCX (default style)
│   ├── template_parser.py       # Extracts style from uploaded DOCX
│   ├── cover_letter.py          # Generates cover letter PDF
│   ├── linkedin_parser.py       # Parses LinkedIn PDF
│   └── config.py                # Loads config.yaml
├── data/                        # Your personal files — gitignored
├── output/                      # Generated resumes — gitignored
├── config.yaml                  # Your personal details — gitignored
├── config.example.yaml          # Template for others ✅
├── .env                         # Your API tokens — gitignored
├── .env.example                 # Template for others ✅
├── requirements.txt             # Python libraries for Windows
├── requirements-mac.txt         # Python libraries for Mac/Linux
├── setup-mac.sh                 # One-click setup for Mac
└── setup-windows.bat            # One-click setup for Windows
```

---

## ❓ Troubleshooting

### Mac: `soffice: command not found`
LibreOffice is not in PATH. Run:
```bash
echo 'export PATH="/Applications/LibreOffice.app/Contents/MacOS:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

### Mac: `permission denied: ./setup-mac.sh`
```bash
chmod +x setup-mac.sh && ./setup-mac.sh
```

### `ModuleNotFoundError: No module named 'utils'`
You are running from the wrong folder. Always run from the **project root**:
```bash
cd resumeai
uvicorn backend.main:app --reload
```

### `401 Invalid token` error
Your HuggingFace or GitHub token is wrong/expired. Create a new one and update `.env`.

### `402 Credits exhausted` error
Your HuggingFace free credits ran out for the month. Create a new free account or wait for the monthly reset.

### Windows: `pythoncom not found`
```
pip install pywin32
```

### Resume is 2 pages
Run again — the AI generates slightly different lengths each time. Also make sure your master resume text is not too long.

---

## 🤝 Contributing

1. Fork the repo
2. Create a branch: `git checkout -b feature/your-feature`
3. Commit: `git commit -m "Add: your feature"`
4. Push: `git push origin feature/your-feature`
5. Open a Pull Request

### Good first issues to work on
- [ ] Add OpenAI / Ollama as alternative LLM providers
- [ ] Add light mode
- [ ] Add job application tracker
- [ ] Add resume history / saved resumes
- [ ] Write unit tests

---

## 📄 License

MIT — free to use, modify, and distribute.

---

<div align="center">
  Made with ❤️ by <a href="https://github.com/varshith-sai">Varshith Sai</a><br><br>
  If this helped you, please ⭐ star the repo!
</div>
