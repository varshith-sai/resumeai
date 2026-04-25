import { useState, useRef } from "react"
import { motion, AnimatePresence } from "framer-motion"
import { Plus, Trash2, Eye, EyeOff, ExternalLink, ChevronRight, Upload, Check } from "lucide-react"

const steps = ["Personal Info", "Education", "API Tokens", "Resume & Files"]

export default function Setup({ onComplete }) {
  const [step, setStep] = useState(0)

  // Use refs for raw input values to avoid controlled input conflicts
  const phoneRef = useRef("")
  const githubRef = useRef("")

  const [personal, setPersonal] = useState({
    name: "", phone: "", email: "", location: "",
    linkedin: "", github: "", github_username: ""
  })
  const [education, setEducation] = useState([
    { degree: "", school: "", dates: "", gpa: "" }
  ])
  const [tokens, setTokens] = useState({ hf: "", github: "" })
  const [showHf, setShowHf] = useState(false)
  const [showGithub, setShowGithub] = useState(false)
  const [masterResumeText, setMasterResumeText] = useState("")
  const [linkedinFile, setLinkedinFile] = useState(null)
  const [resumeTemplateFile, setResumeTemplateFile] = useState(null)
  const [uploading, setUploading] = useState(false)

  // Phone: format only on blur, type freely
  const handlePhoneBlur = () => {
    const raw = phoneRef.current
    const digits = raw.replace(/\D/g, "").slice(0, 11)
    let formatted = ""
    if (digits.length === 0) {
      formatted = ""
    } else if (digits.length <= 1) {
      formatted = `+${digits}`
    } else if (digits.length <= 4) {
      formatted = `+${digits[0]} (${digits.slice(1)}`
    } else if (digits.length <= 7) {
      formatted = `+${digits[0]} (${digits.slice(1, 4)}) ${digits.slice(4)}`
    } else {
      formatted = `+${digits[0]} (${digits.slice(1, 4)}) ${digits.slice(4, 7)}-${digits.slice(7, 11)}`
    }
    phoneRef.current = formatted
    setPersonal(prev => ({ ...prev, phone: formatted }))
  }

  // GitHub: extract username only on blur
  const handleGithubBlur = () => {
    const val = githubRef.current.trim().replace(/\/$/, "")
    const segments = val.split("/").filter(Boolean)
    const username = segments.length >= 3 ? segments[segments.length - 1] : ""
    githubRef.current = val
    setPersonal(prev => ({ ...prev, github: val, github_username: username }))
  }

  const addEducation = () => {
    setEducation(prev => [...prev, { degree: "", school: "", dates: "", gpa: "" }])
  }

  const updateEducation = (i, field, value) => {
    setEducation(prev => {
      const updated = [...prev]
      updated[i] = { ...updated[i], [field]: value }
      return updated
    })
  }

  const removeEducation = (i) => {
    setEducation(prev => prev.filter((_, idx) => idx !== i))
  }

  const handleComplete = async () => {
    setUploading(true)
    const formData = new FormData()
    formData.append("personal", JSON.stringify(personal))
    formData.append("education", JSON.stringify(education))
    formData.append("hf_token", tokens.hf)
    formData.append("github_token", tokens.github)
    formData.append("master_resume_text", masterResumeText)
    if (linkedinFile) formData.append("linkedin_file", linkedinFile)
    if (resumeTemplateFile) formData.append("resume_template_file", resumeTemplateFile)

    try {
      const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000"
      await fetch(`${API_URL}/setup`, { method: "POST", body: formData })
      localStorage.setItem("resumeai_tokens", JSON.stringify(tokens))
      localStorage.setItem("resumeai_personal", JSON.stringify(personal))
      localStorage.setItem("resumeai_education", JSON.stringify(education))
      localStorage.setItem("resumeai_setup_done", "true")
      onComplete({ personal, education, tokens })
    } catch (err) {
      console.error("Setup failed:", err)
    } finally {
      setUploading(false)
    }
  }

  const inputClass =
    "w-full bg-transparent border border-[#1e1e3a] rounded-lg px-4 py-2.5 text-sm text-gray-200 placeholder-gray-600 focus:outline-none focus:border-[#6c63ff] transition-colors"

  return (
    <div className="min-h-screen flex items-center justify-center px-4" style={{ background: "#0d0d1a" }}>
      <motion.div
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        className="w-full max-w-xl"
      >
        {/* Header */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-14 h-14 rounded-2xl gradient-bg mb-4">
            <span className="text-2xl">✨</span>
          </div>
          <h1 className="text-3xl font-bold gradient-text mb-2">Welcome to ResumeAI</h1>
          <p className="text-gray-500 text-sm">Let's set up your profile in a few steps</p>
        </div>

        {/* Progress steps */}
        <div className="flex items-center justify-between mb-8">
          {steps.map((s, i) => (
            <div key={s} className="flex items-center">
              <div className="flex flex-col items-center">
                <motion.div
                  animate={{
                    background: i <= step
                      ? "linear-gradient(135deg, #6c63ff, #3ecfcf)"
                      : "#1e1e3a",
                    scale: i === step ? 1.1 : 1,
                  }}
                  className="w-8 h-8 rounded-full flex items-center justify-center text-xs font-bold"
                >
                  {i < step
                    ? <Check size={14} color="white" />
                    : <span style={{ color: i <= step ? "white" : "#555" }}>{i + 1}</span>
                  }
                </motion.div>
                <span className="text-xs mt-1.5" style={{ color: i === step ? "#6c63ff" : "#555" }}>
                  {s}
                </span>
              </div>
              {i < steps.length - 1 && (
                <div className="w-16 h-px mx-2 mb-5"
                  style={{ background: i < step ? "#6c63ff" : "#1e1e3a" }}
                />
              )}
            </div>
          ))}
        </div>

        {/* Step content */}
        <div className="card glow p-6 mb-4">
          <AnimatePresence mode="wait">

            {/* STEP 0 — Personal Info */}
            {step === 0 && (
              <motion.div
                key="step0"
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -20 }}
              >
                <h2 className="text-base font-semibold text-gray-200 mb-4">Personal Information</h2>
                <div className="space-y-3">

                  <input
                    className={inputClass}
                    placeholder="Full Name *"
                    defaultValue={personal.name}
                    onBlur={(e) => setPersonal(prev => ({ ...prev, name: e.target.value }))}
                  />

                  <input
                    className={inputClass}
                    placeholder="Email *"
                    defaultValue={personal.email}
                    onBlur={(e) => setPersonal(prev => ({ ...prev, email: e.target.value }))}
                  />

                  <input
                    className={inputClass}
                    placeholder="+1 (000) 000-0000"
                    defaultValue={personal.phone}
                    onChange={(e) => { phoneRef.current = e.target.value }}
                    onBlur={handlePhoneBlur}
                  />

                  <input
                    className={inputClass}
                    placeholder="Location e.g. New York, NY"
                    defaultValue={personal.location}
                    onBlur={(e) => setPersonal(prev => ({ ...prev, location: e.target.value }))}
                  />

                  <input
                    className={inputClass}
                    placeholder="LinkedIn URL e.g. https://linkedin.com/in/username"
                    defaultValue={personal.linkedin}
                    onBlur={(e) => setPersonal(prev => ({ ...prev, linkedin: e.target.value }))}
                  />

                  <input
                    className={inputClass}
                    placeholder="GitHub URL e.g. https://github.com/username"
                    defaultValue={personal.github}
                    onChange={(e) => { githubRef.current = e.target.value }}
                    onBlur={handleGithubBlur}
                  />
                  {personal.github_username && (
                    <p className="text-xs text-[#6c63ff] pl-1">
                      ✓ Username detected: <strong>{personal.github_username}</strong>
                    </p>
                  )}

                </div>
              </motion.div>
            )}

            {/* STEP 1 — Education */}
            {step === 1 && (
              <motion.div
                key="step1"
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -20 }}
              >
                <h2 className="text-base font-semibold text-gray-200 mb-4">Education</h2>
                {education.map((edu, i) => (
                  <div key={i} className="mb-4 p-4 rounded-xl"
                    style={{ background: "#0d0d1a", border: "1px solid #1e1e3a" }}>
                    <div className="flex justify-between items-center mb-3">
                      <span className="text-xs text-gray-500">Degree {i + 1}</span>
                      {i > 0 && (
                        <button onClick={() => removeEducation(i)}>
                          <Trash2 size={14} color="#f44336" />
                        </button>
                      )}
                    </div>
                    <div className="space-y-2">
                      <input
                        className={inputClass}
                        placeholder="Degree e.g. B.S. Computer Science *"
                        value={edu.degree}
                        onChange={(e) => updateEducation(i, "degree", e.target.value)}
                      />
                      <input
                        className={inputClass}
                        placeholder="University/School *"
                        value={edu.school}
                        onChange={(e) => updateEducation(i, "school", e.target.value)}
                      />
                      <input
                        className={inputClass}
                        placeholder="Dates e.g. Aug 2022 - May 2026"
                        value={edu.dates}
                        onChange={(e) => updateEducation(i, "dates", e.target.value)}
                      />
                      <input
                        className={inputClass}
                        placeholder="GPA (optional)"
                        value={edu.gpa}
                        onChange={(e) => updateEducation(i, "gpa", e.target.value)}
                      />
                    </div>
                  </div>
                ))}
                <button
                  onClick={addEducation}
                  className="flex items-center gap-1.5 text-xs text-[#6c63ff] mt-2"
                >
                  <Plus size={13} /> Add another degree
                </button>
              </motion.div>
            )}

            {/* STEP 2 — API Tokens */}
            {step === 2 && (
              <motion.div
                key="step2"
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -20 }}
              >
                <h2 className="text-base font-semibold text-gray-200 mb-1">API Tokens</h2>
                <p className="text-xs text-gray-500 mb-4">
                  Saved in your browser (localStorage). Sent to the API only over HTTPS
                  when you run setup or generate.
                </p>

                {/* HF Token */}
                <div className="mb-4">
                  <div className="flex justify-between mb-1.5">
                    <label className="text-xs text-gray-400 font-medium">HuggingFace Token *</label>
                    <a href="https://huggingface.co/settings/tokens" target="_blank"
                      className="text-xs text-[#6c63ff] flex items-center gap-1">
                      Get token <ExternalLink size={10} />
                    </a>
                  </div>
                  <div className="relative">
                    <input
                      type={showHf ? "text" : "password"}
                      placeholder="hf_..."
                      value={tokens.hf}
                      onChange={(e) => setTokens(prev => ({ ...prev, hf: e.target.value }))}
                      className={inputClass + " pr-10"}
                    />
                    <button
                      onClick={() => setShowHf(!showHf)}
                      className="absolute right-3 top-3 text-gray-500"
                    >
                      {showHf ? <EyeOff size={14} /> : <Eye size={14} />}
                    </button>
                  </div>
                  <p className="text-xs text-gray-600 mt-1">
                    Enable "Make calls to Inference Providers" permission
                  </p>
                </div>

                {/* GitHub Token */}
                <div>
                  <div className="flex justify-between mb-1.5">
                    <label className="text-xs text-gray-400 font-medium">GitHub Token *</label>
                    <a href="https://github.com/settings/tokens" target="_blank"
                      className="text-xs text-[#6c63ff] flex items-center gap-1">
                      Get token <ExternalLink size={10} />
                    </a>
                  </div>
                  <div className="relative">
                    <input
                      type={showGithub ? "text" : "password"}
                      placeholder="ghp_..."
                      value={tokens.github}
                      onChange={(e) => setTokens(prev => ({ ...prev, github: e.target.value }))}
                      className={inputClass + " pr-10"}
                    />
                    <button
                      onClick={() => setShowGithub(!showGithub)}
                      className="absolute right-3 top-3 text-gray-500"
                    >
                      {showGithub ? <EyeOff size={14} /> : <Eye size={14} />}
                    </button>
                  </div>
                  <p className="text-xs text-gray-600 mt-1">Enable "public_repo" scope</p>
                </div>
              </motion.div>
            )}

            {/* STEP 3 — Resume & Files */}
            {step === 3 && (
              <motion.div
                key="step3"
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -20 }}
              >
                <h2 className="text-base font-semibold text-gray-200 mb-4">Resume & Files</h2>

                {/* Master Resume Text */}
                <div className="mb-4">
                  <label className="text-xs text-gray-400 font-medium block mb-1.5">
                    Master Resume * (paste your full resume text)
                  </label>
                  <textarea
                    placeholder="Paste your full resume here — experience, skills, projects, awards..."
                    value={masterResumeText}
                    onChange={(e) => setMasterResumeText(e.target.value)}
                    rows={5}
                    className={inputClass + " resize-none"}
                  />
                </div>

                {/* Resume Template DOCX Upload */}
                <div className="mb-4">
                  <label className="text-xs text-gray-400 font-medium block mb-1.5">
                    Your Resume Template (optional)
                  </label>
                  <label
                    className="flex items-center gap-3 p-3 rounded-xl cursor-pointer"
                    style={{
                      background: "#0d0d1a",
                      border: resumeTemplateFile ? "1px dashed #6c63ff" : "1px dashed #2a2a4a"
                    }}
                  >
                    <Upload size={16} color="#6c63ff" />
                    <div className="flex-1">
                      <p className="text-sm" style={{ color: resumeTemplateFile ? "#6c63ff" : "#666" }}>
                        {resumeTemplateFile ? resumeTemplateFile.name : "Upload your existing DOCX resume"}
                      </p>
                      <p className="text-xs text-gray-600 mt-0.5">
                        We'll copy your exact fonts, colors, spacing and layout
                      </p>
                    </div>
                    {resumeTemplateFile && <Check size={16} color="#6c63ff" />}
                    <input
                      type="file"
                      accept=".docx"
                      className="hidden"
                      onChange={(e) => setResumeTemplateFile(e.target.files[0])}
                    />
                  </label>
                  <p className="text-xs mt-1 pl-1" style={{ color: resumeTemplateFile ? "#6c63ff" : "#555" }}>
                    {resumeTemplateFile
                      ? "✓ Template uploaded — your resume style will be matched exactly"
                      : "If skipped, a clean default style will be used"}
                  </p>
                </div>

                {/* LinkedIn PDF Upload */}
                <div>
                  <label className="text-xs text-gray-400 font-medium block mb-1.5">
                    LinkedIn Profile PDF (optional)
                  </label>
                  <label
                    className="flex items-center gap-3 p-3 rounded-xl cursor-pointer"
                    style={{
                      background: "#0d0d1a",
                      border: linkedinFile ? "1px dashed #6c63ff" : "1px dashed #2a2a4a"
                    }}
                  >
                    <Upload size={16} color="#6c63ff" />
                    <div className="flex-1">
                      <p className="text-sm" style={{ color: linkedinFile ? "#6c63ff" : "#666" }}>
                        {linkedinFile ? linkedinFile.name : "Upload LinkedIn PDF"}
                      </p>
                      <p className="text-xs text-gray-600 mt-0.5">
                        Imports your certifications and courses automatically
                      </p>
                    </div>
                    {linkedinFile && <Check size={16} color="#6c63ff" />}
                    <input
                      type="file"
                      accept=".pdf"
                      className="hidden"
                      onChange={(e) => setLinkedinFile(e.target.files[0])}
                    />
                  </label>
                  <p className="text-xs text-gray-600 mt-1 pl-1">
                    LinkedIn → More → Save to PDF
                  </p>
                </div>

              </motion.div>
            )}

          </AnimatePresence>
        </div>

        {/* Navigation buttons */}
        <div className="flex gap-3">
          {step > 0 && (
            <motion.button
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              onClick={() => setStep(step - 1)}
              className="flex-1 py-3 rounded-xl text-sm font-medium text-gray-400"
              style={{ background: "#13131f", border: "1px solid #1e1e3a" }}
            >
              Back
            </motion.button>
          )}
          <motion.button
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            onClick={() => step < steps.length - 1 ? setStep(step + 1) : handleComplete()}
            disabled={uploading}
            className="flex-1 py-3 rounded-xl text-sm font-medium text-white gradient-bg flex items-center justify-center gap-2 disabled:opacity-50"
          >
            {uploading ? "Setting up..." : step < steps.length - 1 ? (
              <><span>Continue</span><ChevronRight size={15} /></>
            ) : (
              <><Check size={15} /><span>Complete Setup</span></>
            )}
          </motion.button>
        </div>

      </motion.div>
    </div>
  )
}
