import { motion } from 'framer-motion'
import { ArrowRight, Check, FileText, Send, Sparkles, WandSparkles } from 'lucide-react'
import './Hero.css'

function Dashboard() {
  return <div className="dashboard-position"><motion.div className="dashboard" initial={{opacity: 0, y: 32, rotateX: 7}} animate={{opacity: 1, y: 0, rotateX: 0}} transition={{delay: .28, duration: .8}}>
    <div className="dash-top"><span className="tiny-logo"><Sparkles size={12}/></span><span>mimic / your voice</span><i></i><b></b><b></b><b></b></div>
    <div className="dash-body"><aside><span className="side-active">✦ &nbsp; Profile</span><span>◌ &nbsp; Style</span><span>◫ &nbsp; History</span><em>⌘ K</em></aside><section className="dash-content">
      <p className="eyebrow">YOUR VOICE PROFILE</p><h3>Hey, CRUD_CREW <span>✦</span></h3><p className="dash-copy">Your profile is ready to help you respond with confidence.</p>
      <div className="message incoming"><span>AM</span><div><small>Alex · 10:42 AM</small><p>Are we still on for lunch?</p></div></div>
      <div className="thinking"><WandSparkles size={14}/> Mimic is drafting a reply that sounds like you <i></i><i></i><i></i></div>
      <div className="message reply"><span>H</span><div><small>You, via Mimic · now</small><p>Absolutely — I’m running a bit late, but I’ll be there soon. 🙌</p><div className="reply-actions"><button>Regenerate</button><button>Copy</button><button className="send"><Send size={12}/> Send</button></div></div></div>
    </section></div>
  </motion.div></div>
}

export default function Hero() {
  return <section id="top" className="hero"><div className="hero-grid"></div><div className="orb orb-one"></div><div className="orb orb-two"></div>
    <div className="container hero-layout"><div className="hero-copy">
      <motion.div className="pill" initial={{opacity:0, y:10}} animate={{opacity:1,y:0}}><span></span> A MORE THOUGHTFUL WAY TO COMMUNICATE</motion.div>
      <motion.h1 initial={{opacity:0,y:18}} animate={{opacity:1,y:0}} transition={{delay:.1}}>Your voice.<br/><em>Thoughtfully extended.</em></motion.h1>
      <motion.p initial={{opacity:0,y:18}} animate={{opacity:1,y:0}} transition={{delay:.18}}>Mimic helps you respond with the same warmth, clarity, and personality you bring in person—without the pressure of drafting every message from scratch.</motion.p>
      <motion.div className="hero-actions" initial={{opacity:0,y:18}} animate={{opacity:1,y:0}} transition={{delay:.25}}><a className="primary-button" href="/login">Create your voice profile <ArrowRight size={18}/></a><a className="text-button" href="#how-it-works">See how it works <span>↓</span></a></motion.div>
      <div className="trust"><div className="avatars"><b>J</b><b>M</b><b>S</b><b>A</b></div><span>Trusted by founders, creators, and busy professionals</span></div>
    </div><div className="hero-visual"><Dashboard /><div className="float-card profile-card"><span>✦</span><div><small>VOICE PROFILE</small><b>Warm & polished</b></div><Check size={15}/></div><div className="float-card training-card"><div className="pulse"></div><div><small>TRAINING COMPLETE</small><b>2,847 messages learned</b></div></div></div></div>
  </section>
}
