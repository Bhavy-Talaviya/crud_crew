import Landing from './pages/Landing'
import Login from './pages/Login'

export default function App() { return window.location.pathname === '/login' ? <Login /> : <Landing /> }
