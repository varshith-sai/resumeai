import { motion } from "framer-motion"
import { Trash2 } from "lucide-react"

export default function JobCard({ job, index, onChange, onRemove }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      transition={{ duration: 0.3, delay: index * 0.1 }}
      className="card glow p-5 mb-4"
    >
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-2">
          <div className="w-2 h-2 rounded-full gradient-bg" />
          <span className="text-sm text-gray-400 font-medium">Job {index + 1}</span>
        </div>
        {index > 0 && (
          <motion.button
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.9 }}
            onClick={onRemove}
            className="text-gray-500 hover:text-red-400 transition-colors"
          >
            <Trash2 size={16} />
          </motion.button>
        )}
      </div>

      <input
        type="text"
        placeholder="Job title e.g. Data Science Intern at Google"
        value={job.name}
        onChange={(e) => onChange(index, "name", e.target.value)}
        className="w-full bg-transparent border border-[#1e1e3a] rounded-lg px-4 py-2 text-sm text-gray-200 placeholder-gray-600 focus:outline-none focus:border-[#6c63ff] transition-colors mb-3"
      />

      <textarea
        placeholder="Paste the full job description here..."
        value={job.description}
        onChange={(e) => onChange(index, "description", e.target.value)}
        rows={6}
        className="w-full bg-transparent border border-[#1e1e3a] rounded-lg px-4 py-3 text-sm text-gray-200 placeholder-gray-600 focus:outline-none focus:border-[#6c63ff] transition-colors resize-none"
      />
    </motion.div>
  )
}