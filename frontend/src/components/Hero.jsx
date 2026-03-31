import { motion } from "framer-motion"

export default function Hero() {
  return (
    <motion.div
      initial={{ opacity: 0, y: -30 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.8 }}
      className="text-center py-16 px-4"
    >
      {/* Animated background orbs */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <motion.div
          animate={{ x: [0, 30, 0], y: [0, -20, 0] }}
          transition={{ duration: 8, repeat: Infinity, ease: "easeInOut" }}
          className="absolute top-20 left-20 w-72 h-72 rounded-full opacity-10"
          style={{ background: "radial-gradient(circle, #6c63ff, transparent)" }}
        />
        <motion.div
          animate={{ x: [0, -30, 0], y: [0, 20, 0] }}
          transition={{ duration: 10, repeat: Infinity, ease: "easeInOut" }}
          className="absolute bottom-20 right-20 w-96 h-96 rounded-full opacity-10"
          style={{ background: "radial-gradient(circle, #3ecfcf, transparent)" }}
        />
        <motion.div
          animate={{ x: [0, 20, 0], y: [0, 30, 0] }}
          transition={{ duration: 12, repeat: Infinity, ease: "easeInOut" }}
          className="absolute top-1/2 left-1/2 w-64 h-64 rounded-full opacity-5"
          style={{ background: "radial-gradient(circle, #6c63ff, transparent)" }}
        />
      </div>

      {/* Logo */}
      <motion.div
        initial={{ scale: 0 }}
        animate={{ scale: 1 }}
        transition={{ duration: 0.5, delay: 0.2 }}
        className="inline-flex items-center justify-center w-16 h-16 rounded-2xl gradient-bg mb-6 shadow-lg"
      >
        <span className="text-2xl">✨</span>
      </motion.div>

      {/* Title */}
      <motion.h1
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.4 }}
        className="text-5xl font-bold gradient-text mb-4"
      >
        ResumeAI
      </motion.h1>

      {/* Subtitle */}
      <motion.p
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.6 }}
        className="text-gray-400 text-lg max-w-xl mx-auto"
      >
        Generate tailored resumes and cover letters for every job in seconds using AI
      </motion.p>

      {/* Floating tags */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.8 }}
        className="flex flex-wrap justify-center gap-2 mt-6"
      >
        {["ATS Optimized", "GitHub Projects", "Cover Letter", "One Click"].map((tag, i) => (
          <motion.span
            key={tag}
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.8 + i * 0.1 }}
            className="px-3 py-1 rounded-full text-xs font-medium"
            style={{ background: "#1e1e3a", color: "#6c63ff", border: "1px solid #2a2a4a" }}
          >
            {tag}
          </motion.span>
        ))}
      </motion.div>
    </motion.div>
  )
}