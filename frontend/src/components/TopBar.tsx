import { Link } from 'react-router-dom'
import './TopBar.css'
import logo from '../assets/logo.png'

const TopBar = () => {
    return (
        <header className="topbar">
            <Link to="/" className="topbar-left">
                <img src={logo} alt="Rubisko Logo" className="topbar-logo" />
                <span className="topbar-title">The Seaweed Hub</span>
            </Link>
        </header>
    )
}

export default TopBar
