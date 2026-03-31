import { motion } from "framer-motion"

export default function Loader({ message }) {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="flex flex-col items-center justify-center py-12 gap-4"
    >
      <div className="relative w-16 h-16">
        <motion.div
          animate={{ rotate: 360 }}
          transition={{ duration: 1.5, repeat: Infinity, ease: "linear" }}
          className="absolute inset-0 rounded-full border-2 border-transparent border-t-[#6c63ff] border-r-[#3ecfcf]"
        />
        <motion.div
          animate={{ rotate: -360 }}
          transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
          className="absolute inset-2 rounded-full border-2 border-transparent border-b-[#6c63ff]"
        />
        <div className="absolute inset-0 flex items-center justify-center text-lg">✨</div>
      </div>
      <motion.p
        animate={{ opacity: [0.5, 1, 0.5] }}
        transition={{ duration: 2, repeat: Infinity }}
        className="text-gray-400 text-sm"
      >
        {message || "Generating your resume..."}
      </motion.p>
    </motion.div>
  )
}