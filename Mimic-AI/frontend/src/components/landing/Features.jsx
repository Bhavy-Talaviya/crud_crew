import { motion } from 'framer-motion'
import { BrainCircuit, LockKeyhole, MessageCircleMore } from 'lucide-react'

const features = [
  { icon: BrainCircuit, number: '01', title: 'Made to sound like you', text: 'Mimic learns the phrases, pacing, and tone that make your messages feel natural—so every reply feels familiar rather than templated.' },
  { icon: MessageCircleMore, number: '02', title: 'Less effort, more connection', text: 'Turn quick replies into thoughtful conversations without spending extra energy writing every message from scratch.' },
  { icon: LockKeyhole, number: '03', title: 'Built with privacy in mind', text: 'Your information stays in your control. The experience is designed to respect your voice and your data.' }
]
export default function Features() {
 return <section className="features section" id="features"><div className="container"><div className="section-heading"><div><p className="eyebrow">BUILT FOR HUMAN CONNECTION</p><h2>More of your voice.<br/><i>Less of the effort.</i></h2></div><p>Technology should support your relationships, not replace the care behind them. Mimic helps with the small things so you can focus on the conversation.</p></div><div className="feature-grid">{features.map(({icon: Icon, number, title, text}, i) => <motion.article className="feature-card" key={title} initial={{opacity:0,y:25}} whileInView={{opacity:1,y:0}} viewport={{once:true}} transition={{delay:i*.12}}><div className="feature-icon"><Icon size={23}/><span>{number}</span></div><h3>{title}</h3><p>{text}</p><a href="#start">Explore <span>→</span></a></motion.article>)}</div></div></section>
}
