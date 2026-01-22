import { useState, useEffect } from 'react'
import { Link, useLocation } from 'react-router-dom'
import './Sidebar.css'

interface MenuItem {
    id: string
    label: string
    icon: string
    path: string
}

const menuItems: MenuItem[] = [
    { id: 'quality-control', label: 'Quality Control', icon: '🔬', path: '/quality-control' },
]

const Sidebar = () => {
    const [isCollapsed, setIsCollapsed] = useState(false)
    const location = useLocation()

    useEffect(() => {
        // Automatically collapse sidebar if not on the home page
        if (location.pathname !== '/') {
            setIsCollapsed(true)
        } else {
            setIsCollapsed(false)
        }
    }, [location.pathname])

    return (
        <aside className={`sidebar ${isCollapsed ? 'collapsed' : ''}`}>
            <div className="sidebar-header">
                <button
                    className="collapse-button"
                    onClick={() => setIsCollapsed(!isCollapsed)}
                    title={isCollapsed ? 'Expand sidebar' : 'Collapse sidebar'}
                >
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                        <line x1="3" y1="12" x2="21" y2="12"></line>
                        <line x1="3" y1="6" x2="21" y2="6"></line>
                        <line x1="3" y1="18" x2="21" y2="18"></line>
                    </svg>
                </button>
            </div>
            <nav className="sidebar-nav">
                {menuItems.map((item) => (
                    <Link
                        key={item.id}
                        to={item.path}
                        className={`menu-item ${location.pathname === item.path ? 'active' : ''}`}
                        title={isCollapsed ? item.label : ''}
                    >
                        <span className="menu-icon">{item.icon}</span>
                        {!isCollapsed && <span className="menu-label">{item.label}</span>}
                    </Link>
                ))}
            </nav>
        </aside>
    )
}

export default Sidebar
