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
    <nav className="bg-white border-b border-gray-200 px-6 py-3 flex justify-between items-center">
      <div className="flex items-center gap-6">
        <Link to="/" className="text-lg font-semibold text-gray-800">
          Research Copilot
        </Link>

        {user && (
          <div className="flex items-center gap-4 text-sm">
            <Link to="/dashboard" className="text-gray-600 hover:text-gray-900">
              Dashboard
            </Link>
            <Link to="/research-interests" className="text-gray-600 hover:text-gray-900">
              Research Interests
            </Link>
          </div>
        )}
      </div>

      {user && (
        <div className="flex items-center gap-4">
          <span className="text-sm text-gray-600">{user.full_name || user.email}</span>
          <button
            onClick={handleLogout}
            className="text-sm px-3 py-1.5 rounded-md bg-gray-100 hover:bg-gray-200 text-gray-700"
          >
            Logout
          </button>
        </div>
      )}
    </nav>
  )
}