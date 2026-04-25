import { useState } from "react"
import { motion, AnimatePresence } from "framer-motion"
import { Settings, Eye, EyeOff, X, ExternalLink } from "lucide-react"

export default function SettingsPanel({ tokens, onSave }) {
  const [open, setOpen] = useState(false)
  const [hfToken, setHfToken] = useState(tokens.hf || "")
  const [githubToken, setGithubToken] = useState(tokens.github || "")
  const [showHf, setShowHf] = useState(false)
  const [showGithub, setShowGithub] = useState(false)

  const save = () => {
    onSave({ hf: hfToken, github: githubToken })
    setOpen(false)
  }

  return (
    <>
      <motion.button
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
        onClick={() => setOpen(true)}
        className="fixed top-4 right-4 z-50 p-2.5 rounded-xl"
        style={{ background: "#13131f", border: "1px solid #1e1e3a" }}
      >
        <Settings size={18} color="#6c63ff" />
      </motion.button>

      <AnimatePresence>
        {open && (
          <>
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onClick={() => setOpen(false)}
              className="fixed inset-0 z-40"
              style={{ background: "rgba(0,0,0,0.7)" }}
            />
            <motion.div
              initial={{ opacity: 0, scale: 0.95, y: -20 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.95, y: -20 }}
              className="fixed top-16 right-4 z-50 w-96 card glow p-6"
            >
              <div className="flex items-center justify-between mb-5">
                <h3 className="font-semibold text-gray-100">API Settings</h3>
                <button onClick={() => setOpen(false)}>
                  <X size={16} color="#666" />
                </button>
              </div>

              <div className="mb-4">
                <div className="flex items-center justify-between mb-1.5">
                  <label className="text-xs text-gray-400 font-medium">HuggingFace Token</label>
                  <a href="https://huggingface.co/settings/tokens" target="_blank"
                    className="text-xs text-[#6c63ff] flex items-center gap-1">
                    Get token <ExternalLink size={10} />
                  </a>
                </div>
                <div className="relative">
                  <input
                    type={showHf ? "text" : "password"}
                    placeholder="hf_..."
                    value={hfToken}
                    onChange={(e) => setHfToken(e.target.value)}
                    className="w-full bg-transparent border border-[#1e1e3a] rounded-lg px-4 py-2 text-sm text-gray-200 placeholder-gray-600 focus:outline-none focus:border-[#6c63ff] pr-10"
                  />
                  <button onClick={() => setShowHf(!showHf)}
                    className="absolute right-3 top-2.5 text-gray-500">
                    {showHf ? <EyeOff size={14} /> : <Eye size={14} />}
                  </button>
                </div>
              </div>

              <div className="mb-5">
                <div className="flex items-center justify-between mb-1.5">
                  <label className="text-xs text-gray-400 font-medium">GitHub Token</label>
                  <a href="https://github.com/settings/tokens" target="_blank"
                    className="text-xs text-[#6c63ff] flex items-center gap-1">
                    Get token <ExternalLink size={10} />
                  </a>
                </div>
                <div className="relative">
                  <input
                    type={showGithub ? "text" : "password"}
                    placeholder="ghp_..."
                    value={githubToken}
                    onChange={(e) => setGithubToken(e.target.value)}
                    className="w-full bg-transparent border border-[#1e1e3a] rounded-lg px-4 py-2 text-sm text-gray-200 placeholder-gray-600 focus:outline-none focus:border-[#6c63ff] pr-10"
                  />
                  <button onClick={() => setShowGithub(!showGithub)}
                    className="absolute right-3 top-2.5 text-gray-500">
                    {showGithub ? <EyeOff size={14} /> : <Eye size={14} />}
                  </button>
                </div>
              </div>

              <p className="text-xs text-gray-600 mb-4">
                Tokens stay in your browser and are sent only when needed for API calls.
              </p>

              <motion.button
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                onClick={save}
                className="w-full py-2.5 rounded-xl text-white text-sm font-medium gradient-bg"
              >
                Save Settings
              </motion.button>
            </motion.div>
          </>
        )}
      </AnimatePresence>
    </>
  )
}