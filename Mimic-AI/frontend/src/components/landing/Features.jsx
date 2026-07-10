import { motion } from 'framer-motion'
import { BrainCircuit, LockKeyhole, MessageCircleMore } from 'lucide-react'

const features = [
  { icon: BrainCircuit, number: '01', title: 'Unmistakably you', text: 'Mimic picks up on the details that make your messages feel like yours — from your favorite phrases to the way you use emojis.' },
  { icon: MessageCircleMore, number: '02', title: 'Present, without the pressure', text: 'Draft replies that sound natural and thoughtful, so the people who matter never get a version of you that feels generic.' },
  { icon: LockKeyhole, number: '03', title: 'Private by design', text: 'Your conversations stay yours. Your clone is trained locally and your data is never used to train public models.' }
]
export default function Features() {
 return <section className="features section" id="features"><div className="container"><div className="section-heading"><div><p className="eyebrow">BUILT FOR HUMAN CONNECTION</p><h2>More you.<br/><i>Less typing.</i></h2></div><p>Technology should make us feel more human, not less. Mimic handles the small stuff, so you can focus on what matters.</p></div><div className="feature-grid">{features.map(({icon: Icon, number, title, text}, i) => <motion.article className="feature-card" key={title} initial={{opacity:0,y:25}} whileInView={{opacity:1,y:0}} viewport={{once:true}} transition={{delay:i*.12}}><div className="feature-icon"><Icon size={23}/><span>{number}</span></div><h3>{title}</h3><p>{text}</p><a href="#start">Explore <span>→</span></a></motion.article>)}</div></div></section>
}
