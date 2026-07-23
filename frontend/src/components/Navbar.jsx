import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

export default function Navbar() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <nav className="sticky top-0 z-20 border-b border-slate-200/80 bg-white/95 backdrop-blur supports-[backdrop-filter]:bg-white/80">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-4 py-3 sm:px-6 lg:px-8">
        <div className="flex items-center gap-6">
          <Link to="/" className="text-base font-semibold tracking-tight text-slate-900">
            Research Copilot
          </Link>

          {user && (
            <div className="hidden items-center gap-5 text-sm text-slate-600 md:flex">
              <Link to="/dashboard" className="transition-colors hover:text-slate-900">
                Dashboard
              </Link>
              <Link to="/research-interests" className="transition-colors hover:text-slate-900">
                Research Interests
              </Link>
              <Link to="/settings" className="transition-colors hover:text-slate-900">
                Settings
              </Link>
            </div>
          )}
        </div>

        {user && (
          <div className="flex items-center gap-3">
            <span className="hidden rounded-full bg-slate-100 px-3 py-1 text-sm text-slate-600 sm:inline-flex">
              {user.full_name || user.email}
            </span>
            <button
              onClick={handleLogout}
              className="rounded-md border border-slate-200 px-3 py-1.5 text-sm font-medium text-slate-700 transition-colors hover:bg-slate-50"
            >
              Logout
            </button>
          </div>
        )}
      </div>
    </nav>
  )
}