import { motion } from "framer-motion"
import { Download, FileText, AlertCircle } from "lucide-react"

export default function ResultCard({ result, index, apiUrl }) {
  const downloadFile = (path, filename) => {
    const url = `${apiUrl}/download?path=${encodeURIComponent(path)}`
    const a = document.createElement("a")
    a.href = url
    a.download = filename
    a.click()
  }

  const atsColor = result.score?.ats_score >= 85
    ? "#4caf50" : result.score?.ats_score >= 70
    ? "#ff9800" : "#f44336"

  const atsBg = result.score?.ats_score >= 85
    ? "#1a472a" : result.score?.ats_score >= 70
    ? "#3d2a00" : "#3d0000"

  return (
    <motion.div
      initial={{ opacity: 0, y: 30 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: index * 0.15 }}
      className="card glow p-6 mb-4"
    >
      {/* Header */}
      <div className="flex items-center gap-3 mb-4">
        <div className="w-10 h-10 rounded-xl gradient-bg flex items-center justify-center">
          <FileText size={18} color="white" />
        </div>
        <div>
          <h3 className="font-semibold text-gray-100">{result.name}</h3>
          <p className="text-xs text-gray-500">Resume generated</p>
        </div>
        {result.score && (
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ delay: 0.3 + index * 0.15 }}
            className="ml-auto px-4 py-1.5 rounded-full text-sm font-bold"
            style={{ background: atsBg, color: atsColor }}
          >
            ATS {result.score.ats_score}/100
          </motion.div>
        )}
      </div>

      {result.error ? (
        <div className="flex items-center gap-2 text-red-400 text-sm">
          <AlertCircle size={16} />
          {result.error}
        </div>
      ) : (
        <>
          {/* Keywords */}
          {result.score && (
            <div className="grid grid-cols-2 gap-4 mb-5">
              <div>
                <p className="text-xs text-gray-500 mb-2 font-medium">✅ MATCHED</p>
                <div className="flex flex-wrap gap-1">
                  {result.score.matched_keywords.map((k) => (
                    <span
                      key={k}
                      className="px-2 py-0.5 rounded-full text-xs"
                      style={{ background: "#1a472a", color: "#4caf50" }}
                    >
                      {k}
                    </span>
                  ))}
                </div>
              </div>
              <div>
                <p className="text-xs text-gray-500 mb-2 font-medium">❌ MISSING</p>
                <div className="flex flex-wrap gap-1">
                  {result.score.missing_keywords.length === 0 ? (
                    <span className="px-2 py-0.5 rounded-full text-xs"
                      style={{ background: "#1a472a", color: "#4caf50" }}>
                      None 🎉
                    </span>
                  ) : result.score.missing_keywords.map((k) => (
                    <span
                      key={k}
                      className="px-2 py-0.5 rounded-full text-xs"
                      style={{ background: "#3d0000", color: "#f44336" }}
                    >
                      {k}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* Download buttons */}
          <div className="flex gap-3">
            {result.pdf_path && (
              <motion.button
                whileHover={{ scale: 1.03 }}
                whileTap={{ scale: 0.97 }}
                onClick={() => downloadFile(result.pdf_path,
                  result.name.replace(/ /g, "_") + "_resume.pdf")}
                className="flex-1 flex items-center justify-center gap-2 py-2.5 rounded-xl text-sm font-medium gradient-bg text-white"
              >
                <Download size={15} />
                Resume PDF
              </motion.button>
            )}
            {result.cover_letter_path && (
              <motion.button
                whileHover={{ scale: 1.03 }}
                whileTap={{ scale: 0.97 }}
                onClick={() => downloadFile(result.cover_letter_path,
                  result.name.replace(/ /g, "_") + "_cover_letter.pdf")}
                className="flex-1 flex items-center justify-center gap-2 py-2.5 rounded-xl text-sm font-medium text-gray-200"
                style={{ background: "#1e1e3a", border: "1px solid #2a2a4a" }}
              >
                <Download size={15} />
                Cover Letter
              </motion.button>
            )}
          </div>
        </>
      )}
    </motion.div>
  )
}