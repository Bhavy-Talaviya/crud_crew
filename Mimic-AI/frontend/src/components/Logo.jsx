import { motion } from 'framer-motion'
import './Logo.css'

export default function Logo({ compact }) {
  return (
    <motion.div
      className={`mimic-logo ${compact ? 'compact' : ''}`}
      initial={{ opacity: 0, y: -8 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ type: 'spring', stiffness: 300, damping: 22 }}
    >
      <span className="mimic-text" data-text="Mimic">Mimic</span>
      <span className="mimic-ai">AI</span>
    </motion.div>
  )
}
