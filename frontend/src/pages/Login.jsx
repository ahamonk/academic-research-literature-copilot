import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

export default function Login() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const { login } = useAuth()
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    try {
      await login(email, password)
      navigate('/dashboard')
    } catch {
      setError('Invalid email or password.')
    }
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-slate-50 px-4 py-10">
      <div className="grid w-full max-w-5xl overflow-hidden rounded-[28px] border border-slate-200 bg-white shadow-sm lg:grid-cols-[1.1fr_0.9fr]">
        <div className="hidden bg-slate-900 p-10 text-white lg:flex lg:flex-col lg:justify-between">
          <div>
            <p className="text-sm font-semibold uppercase tracking-[0.24em] text-slate-300">
              Research Copilot
            </p>
            <h1 className="mt-4 text-3xl font-semibold tracking-tight">
              Welcome back to your research workspace.
            </h1>
            <p className="mt-3 max-w-sm text-sm leading-6 text-slate-300">
              Follow the latest literature, organize topics, and keep your review workflow moving.
            </p>
          </div>
          <div className="text-sm text-slate-400">
            Secure sign-in for your academic dashboard.
          </div>
        </div>

        <div className="p-8 sm:p-10">
          <form onSubmit={handleSubmit} className="mx-auto w-full max-w-sm">
            <h2 className="text-2xl font-semibold tracking-tight text-slate-900">Log in</h2>
            <p className="mt-2 text-sm leading-6 text-slate-600">
              Access your saved topics, weekly reviews, and search workspace.
            </p>

            {error && (
              <div className="mt-5 rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
                {error}
              </div>
            )}

            <label className="mt-5 block text-sm font-medium text-slate-700">Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              className="mt-2 w-full rounded-xl border border-slate-300 bg-slate-50 px-3 py-2.5 text-sm text-slate-900 outline-none transition focus:border-blue-500 focus:bg-white focus:ring-2 focus:ring-blue-100"
            />

            <label className="mt-4 block text-sm font-medium text-slate-700">Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              className="mt-2 w-full rounded-xl border border-slate-300 bg-slate-50 px-3 py-2.5 text-sm text-slate-900 outline-none transition focus:border-blue-500 focus:bg-white focus:ring-2 focus:ring-blue-100"
            />

            <button
              type="submit"
              className="mt-6 w-full rounded-xl bg-blue-600 px-4 py-2.5 text-sm font-medium text-white transition hover:bg-blue-700"
            >
              Log in
            </button>

            <p className="mt-5 text-center text-sm text-slate-600">
              Don't have an account?{' '}
              <Link to="/register" className="font-medium text-blue-600 transition hover:text-blue-700">
                Register
              </Link>
            </p>
          </form>
        </div>
      </div>
    </div>
  )
}