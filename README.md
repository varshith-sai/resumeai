# ✨ ResumeAI — AI-Powered Resume & Cover Letter Generator

<div align="center">

![ResumeAI Banner](https://img.shields.io/badge/ResumeAI-AI%20Powered-6c63ff?style=for-the-badge&logo=sparkles)
![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi)
![React](https://img.shields.io/badge/React-Frontend-61dafb?style=for-the-badge&logo=react)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Stars](https://img.shields.io/github/stars/varshith-sai/resumeai?style=for-the-badge)
![Forks](https://img.shields.io/github/forks/varshith-sai/resumeai?style=for-the-badge)

**Paste a job description → Get a tailored resume + cover letter in seconds**

[🚀 Try it](#setup) · [🐛 Report Bug](https://github.com/varshith-sai/resumeai/issues) · [💡 Request Feature](https://github.com/varshith-sai/resumeai/issues) · [🤝 Contribute](#contributing)

</div>

---

## 🎯 What is ResumeAI?

ResumeAI is a free, open-source tool that uses AI to generate **tailored resumes and cover letters** for every job you apply to — automatically.

- 🤖 **AI tailors your resume** to match each job description
- 📊 **ATS scoring** shows how well your resume matches keywords
- 🐙 **Auto-pulls your GitHub projects** and selects the most relevant ones
- 💼 **Imports certifications** from your LinkedIn PDF
- 📄 **Exports Resume + Cover Letter as PDF** instantly
- 🎨 **Beautiful modern UI** built with React + Framer Motion

---

## 📸 Screenshots

> Add screenshots here after deploying

---

## ⚡ Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- Microsoft Word (Windows) or LibreOffice (Linux/Mac)
- [HuggingFace account](https://huggingface.co) (free)
- [GitHub account](https://github.com) (free)

### 1. Clone the repo
```bash
git clone https://github.com/varshith-sai/resumeai.git
cd resumeai
```

### 2. Set up Python environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Set up environment variables
```bash
cp .env.example .env
```
Edit `.env` and add your tokens:
- `HF_API_TOKEN` → [Get from HuggingFace](https://huggingface.co/settings/tokens) — enable "Make calls to Inference Providers"
- `GITHUB_TOKEN` → [Get from GitHub](https://github.com/settings/tokens) — enable "public_repo" scope

### 4. Set up config
```bash
cp config.example.yaml config.yaml
```
Edit `config.yaml` with your personal details and education.

### 5. Run the backend
```bash
uvicorn backend.main:app --reload
```

### 6. Run the frontend (new terminal)
```bash
cd frontend
npm install
npm run dev
```

### 7. Open the app
```
http://localhost:5173
```
Complete the setup wizard — add your resume, tokens, and LinkedIn PDF. Done! 🎉

---

## 🌐 Deploying Online (BYOK)

This project supports **BYOK** (Bring Your Own Keys): each user enters their own Hugging Face and GitHub tokens in the UI.

### Backend (Render)

This repo includes a `Dockerfile` with LibreOffice so DOCX to PDF conversion works on Linux hosts.

1. Push this repo to GitHub.
2. In Render, create a service from `render.yaml` (Blueprint) or choose Docker and point to root `Dockerfile`.
3. Set `CORS_ORIGINS` to your frontend URL (example: `https://your-app.vercel.app`).
4. Optional: set `MAX_UPLOAD_BYTES` if you want a different upload size limit.

### Frontend (Vercel)

1. Deploy the `frontend` folder.
2. Set env var `VITE_API_URL` to your backend URL (example: `https://resumeai-backend.onrender.com`).
3. Redeploy after setting env vars.

### Security and behavior notes

- API keys are entered by users and sent only when needed.
- Keys are not committed to git.
- Backend now has rate limits and upload-size limits.
- Download endpoint only serves generated PDF files from `output/`.
- On free hosting plans, server disk may be temporary; users may need to run setup again after a restart.

---

## 🗂️ Project Structure

```
resumeai/
├── backend/
│   └── main.py              # FastAPI endpoints
├── frontend/
│   └── src/
│       ├── App.jsx           # Main app
│       └── components/       # UI components
├── utils/
│   ├── llm.py               # HuggingFace LLM calls
│   ├── github.py            # GitHub project fetcher
│   ├── scorer.py            # ATS keyword scorer
│   ├── generator.py         # Main resume pipeline
│   ├── resume_builder.py    # DOCX builder
│   ├── cover_letter.py      # Cover letter generator
│   ├── linkedin_parser.py   # LinkedIn PDF parser
│   └── config.py            # Config loader
├── data/                    # Your personal data (gitignored)
├── output/                  # Generated resumes (gitignored)
├── config.example.yaml      # Config template
└── .env.example             # Env template
```

---

## 🔑 API Keys Required

| Key | Where to get | Permission needed |
|-----|-------------|-------------------|
| `HF_API_TOKEN` | [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens) | Make calls to Inference Providers |
| `GITHUB_TOKEN` | [github.com/settings/tokens](https://github.com/settings/tokens) | public_repo |

Both are **free** — no credit card needed.

---

## 🤝 Contributing

Contributions are what make open source amazing! Here's how you can help:

### Good first issues to work on
- [ ] Add support for OpenAI / Ollama as LLM providers
- [ ] Add dark/light mode toggle
- [ ] Add job application tracker
- [ ] Add resume history / saved resumes
- [ ] Add support for uploading existing resume (DOCX/PDF) instead of pasting text
- [ ] Improve ATS scoring accuracy
- [ ] Add more resume templates
- [ ] Write unit tests

### How to contribute

1. **Fork** the repo
2. **Create** a feature branch
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make** your changes
4. **Commit** with a clear message
   ```bash
   git commit -m "Add: your feature description"
   ```
5. **Push** to your fork
   ```bash
   git push origin feature/your-feature-name
   ```
6. **Open a Pull Request** — describe what you changed and why

### Code style
- Python: follow PEP8, use meaningful variable names
- React: functional components only, use Tailwind for styling
- Keep components small and focused

---

## 🛣️ Roadmap

- [x] AI resume generation
- [x] ATS keyword scoring
- [x] Cover letter generation
- [x] GitHub project integration
- [x] LinkedIn PDF import
- [x] Modern React UI
- [x] User setup wizard
- [ ] Online deployment (Render + Vercel)
- [ ] Job application tracker
- [ ] Multiple LLM providers (OpenAI, Ollama)
- [ ] Resume templates
- [ ] Resume history
- [ ] Chrome extension

---

## 📄 License

MIT License — free to use, modify, and distribute. See [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgements

- [HuggingFace](https://huggingface.co) for free LLM inference
- [FastAPI](https://fastapi.tiangolo.com) for the backend
- [Framer Motion](https://www.framer.com/motion/) for animations
- [python-docx](https://python-docx.readthedocs.io) for DOCX generation

---

<div align="center">
  Made with ❤️ by <a href="https://github.com/varshith-sai">Varshith Sai</a>
  <br><br>
  If this helped you, please ⭐ star the repo — it means a lot!
</div>
