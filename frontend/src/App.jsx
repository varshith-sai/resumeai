import { useState, useEffect } from "react"
import { motion, AnimatePresence } from "framer-motion"
import { Plus, Sparkles } from "lucide-react"
import axios from "axios"
import Hero from "./components/Hero"
import JobCard from "./components/JobCard"
import ResultCard from "./components/ResultCard"
import Loader from "./components/Loader"
import SettingsPanel from "./components/Settings"
import Setup from "./components/Setup"

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000"

export default function App() {
  const [jobs, setJobs] = useState([{ name: "Job 1", description: "" }])
  const [results, setResults] = useState([])
  const [loading, setLoading] = useState(false)
  const [currentJob, setCurrentJob] = useState("")
  const [tokens, setTokens] = useState({ hf: "", github: "" })
  const [setupDone, setSetupDone] = useState(false)

  useEffect(() => {
    const done = localStorage.getItem("resumeai_setup_done")
    const savedTokens = localStorage.getItem("resumeai_tokens")
    if (done) setSetupDone(true)
    if (savedTokens) setTokens(JSON.parse(savedTokens))
  }, [])

  const saveTokens = (newTokens) => {
    setTokens(newTokens)
    localStorage.setItem("resumeai_tokens", JSON.stringify(newTokens))
  }

  const addJob = () => {
    setJobs([...jobs, { name: `Job ${jobs.length + 1}`, description: "" }])
  }

  const removeJob = (index) => {
    setJobs(jobs.filter((_, i) => i !== index))
  }

  const updateJob = (index, field, value) => {
    const updated = [...jobs]
    updated[index][field] = value
    setJobs(updated)
  }

  const generate = async () => {
    const valid = jobs.filter((j) => j.description.trim())
    if (!valid.length) return

    if (!tokens.hf) {
      alert("Please add your HuggingFace token in Settings (top right corner)")
      return
    }

    setLoading(true)
    setResults([])

    try {
      const allResults = []
      for (const job of valid) {
        setCurrentJob(job.name)
        const res = await axios.post(`${API_URL}/generate`, {
          jobs: [job],
          hf_token: tokens.hf,
          github_token: tokens.github
        })
        allResults.push(...res.data.results)
        setResults([...allResults])
      }
    } catch (err) {
      console.error("Generation failed:", err)
      const detail =
        err?.response?.data?.detail ??
        err?.response?.data?.message ??
        err?.message ??
        "Request failed"
      alert(typeof detail === "string" ? detail : JSON.stringify(detail))
    } finally {
      setLoading(false)
      setCurrentJob("")
    }
  }

  // Show setup page on first visit
  if (!setupDone) {
    return (
      <Setup onComplete={(data) => {
        setTokens(data.tokens)
        setSetupDone(true)
      }} />
    )
  }

  return (
    <div className="min-h-screen" style={{ background: "#0d0d1a" }}>

      {/* Settings */}
      <SettingsPanel tokens={tokens} onSave={saveTokens} />

      <div className="max-w-2xl mx-auto px-4 pb-20">

        {/* Hero */}
        <Hero />

        {/* Token warning */}
        <AnimatePresence>
          {!tokens.hf && (
            <motion.div
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0 }}
              className="mb-4 px-4 py-3 rounded-xl text-sm text-yellow-400 flex items-center gap-2"
              style={{ background: "#2a2000", border: "1px solid #3d3000" }}
            >
              ⚠️ Add your HuggingFace token in Settings (top right) to generate resumes
            </motion.div>
          )}
        </AnimatePresence>

        {/* Job Cards */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.5 }}
        >
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-sm font-semibold text-gray-400 uppercase tracking-wider">
              Job Descriptions
            </h2>
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={addJob}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium text-[#6c63ff]"
              style={{ background: "#13131f", border: "1px solid #2a2a4a" }}
            >
              <Plus size={13} />
              Add Job
            </motion.button>
          </div>

          <AnimatePresence>
            {jobs.map((job, i) => (
              <JobCard
                key={i}
                job={job}
                index={i}
                onChange={updateJob}
                onRemove={() => removeJob(i)}
              />
            ))}
          </AnimatePresence>

          {/* Generate Button */}
          <motion.button
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            onClick={generate}
            disabled={loading}
            className="w-full py-4 rounded-2xl text-white font-semibold text-base mt-4 flex items-center justify-center gap-2 gradient-bg disabled:opacity-50"
            style={{ boxShadow: "0 0 30px rgba(108, 99, 255, 0.3)" }}
          >
            <Sparkles size={18} />
            {loading ? "Generating..." : "Generate Resumes"}
          </motion.button>
        </motion.div>

        {/* Loader */}
        <AnimatePresence>
          {loading && (
            <Loader message={`Generating resume for ${currentJob}...`} />
          )}
        </AnimatePresence>

        {/* Results */}
        <AnimatePresence>
          {results.length > 0 && !loading && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="mt-8"
            >
              <h2 className="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-4">
                Your Resumes
              </h2>
              {results.map((result, i) => (
                <ResultCard key={i} result={result} index={i} apiUrl={API_URL} />
              ))}
            </motion.div>
          )}
        </AnimatePresence>

      </div>
    </div>
  )
}