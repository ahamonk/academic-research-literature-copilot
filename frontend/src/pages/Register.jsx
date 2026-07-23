import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

export default function Register() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [fullName, setFullName] = useState('')
  const [error, setError] = useState('')
  const { register } = useAuth()
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    try {
      await register(email, password, fullName)
      navigate('/login')
    } catch (err) {
      const detail = err.response?.data?.detail
      setError(detail || 'Registration failed.')
    }
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-slate-50 px-4 py-10">
      <div className="grid w-full max-w-5xl overflow-hidden rounded-[28px] border border-slate-200 bg-white shadow-sm lg:grid-cols-[1.1fr_0.9fr]">
        <div className="hidden bg-slate-900 p-10 text-white lg:flex lg:flex-col lg:justify-between">
          <div>
            <p className="text-sm font-semibold uppercase tracking-[0.24em] text-slate-300">
              New account
            </p>
            <h1 className="mt-4 text-3xl font-semibold tracking-tight">
              Create your research dashboard profile.
            </h1>
            <p className="mt-3 max-w-sm text-sm leading-6 text-slate-300">
              Set up your preferences and start building a tailored literature workflow.
            </p>
          </div>
          <div className="text-sm text-slate-400">
            Lightweight, professional research planning.
          </div>
        </div>

        <div className="p-8 sm:p-10">
          <form onSubmit={handleSubmit} className="mx-auto w-full max-w-sm">
            <h2 className="text-2xl font-semibold tracking-tight text-slate-900">Create an account</h2>
            <p className="mt-2 text-sm leading-6 text-slate-600">
              Join the workspace to track topics, reviews, and paper discovery.
            </p>

            {error && (
              <div className="mt-5 rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
                {error}
              </div>
            )}

            <label className="mt-5 block text-sm font-medium text-slate-700">Full name</label>
            <input
              type="text"
              value={fullName}
              onChange={(e) => setFullName(e.target.value)}
              className="mt-2 w-full rounded-xl border border-slate-300 bg-slate-50 px-3 py-2.5 text-sm text-slate-900 outline-none transition focus:border-blue-500 focus:bg-white focus:ring-2 focus:ring-blue-100"
            />

            <label className="mt-4 block text-sm font-medium text-slate-700">Email</label>
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
              Register
            </button>

            <p className="mt-5 text-center text-sm text-slate-600">
              Already have an account?{' '}
              <Link to="/login" className="font-medium text-blue-600 transition hover:text-blue-700">
                Log in
              </Link>
            </p>
          </form>
        </div>
      </div>
    </div>
  )
}