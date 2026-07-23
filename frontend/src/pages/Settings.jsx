import { useEffect, useState } from 'react'
import Layout from '../components/Layout'
import { getSlackStatus, getSlackConnectUrl, disconnectSlack, toggleSlack } from '../services/slackService'

export default function Settings() {
  const [status, setStatus] = useState({ connected: false, enabled: false, workspace_name: null })
  const [loading, setLoading] = useState(true)
  const [actionLoading, setActionLoading] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    loadStatus()
  }, [])

  const loadStatus = async () => {
    setLoading(true)
    setError('')
    try {
      const data = await getSlackStatus()
      setStatus(data)
    } catch {
      setError('Failed to load Slack status.')
    } finally {
      setLoading(false)
    }
  }

  const handleConnect = async () => {
    setActionLoading(true)
    setError('')
    try {
      const url = await getSlackConnectUrl()
      window.location.href = url
    } catch {
      setError('Failed to start Slack connection.')
      setActionLoading(false)
    }
  }

  const handleDisconnect = async () => {
    setActionLoading(true)
    setError('')
    try {
      await disconnectSlack()
      await loadStatus()
    } catch {
      setError('Failed to disconnect Slack.')
    } finally {
      setActionLoading(false)
    }
  }

  const handleToggle = async () => {
    setActionLoading(true)
    setError('')
    try {
      const data = await toggleSlack(!status.enabled)
      setStatus(data)
    } catch {
      setError('Failed to update notification setting.')
    } finally {
      setActionLoading(false)
    }
  }

  return (
    <Layout>
      <section className="mb-6 rounded-2xl border border-slate-200 bg-white p-6 shadow-sm sm:p-8">
        <h1 className="text-2xl font-semibold tracking-tight text-slate-900">Settings</h1>
        <p className="mt-2 text-sm leading-6 text-slate-600">
          Manage integrations for your account.
        </p>
      </section>

      <div className="max-w-2xl rounded-2xl border border-slate-200 bg-white p-6 shadow-sm sm:p-8">
        <h2 className="text-lg font-semibold text-slate-900">Slack</h2>
        <p className="mt-2 text-sm text-slate-600">
          Connect your workspace to send weekly review notifications.
        </p>

        {loading && (
          <div className="mt-5 rounded-xl border border-slate-200 bg-slate-50 px-4 py-4 text-sm text-slate-500">
            Loading...
          </div>
        )}
        {error && (
          <div className="mt-5 rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
            {error}
          </div>
        )}

        {!loading && (
          <>
            <div className="mt-6 flex flex-col gap-4 rounded-xl border border-slate-200 bg-slate-50 p-4 sm:flex-row sm:items-center sm:justify-between">
              <div>
                <p className="text-sm font-medium text-slate-700">
                  Status:{' '}
                  <span className={status.connected ? 'text-emerald-600' : 'text-slate-500'}>
                    {status.connected ? 'Connected' : 'Not Connected'}
                  </span>
                </p>
                {status.connected && status.workspace_name && (
                  <p className="mt-1 text-xs text-slate-500">Workspace: {status.workspace_name}</p>
                )}
              </div>

              {status.connected ? (
                <button
                  onClick={handleDisconnect}
                  disabled={actionLoading}
                  className="rounded-xl border border-slate-200 bg-white px-3 py-2 text-sm font-medium text-slate-700 transition hover:bg-slate-50 disabled:cursor-not-allowed disabled:opacity-50"
                >
                  Disconnect Slack
                </button>
              ) : (
                <button
                  onClick={handleConnect}
                  disabled={actionLoading}
                  className="rounded-xl bg-blue-600 px-3 py-2 text-sm font-medium text-white transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-50"
                >
                  Connect Slack
                </button>
              )}
            </div>

            {status.connected && (
              <label className="mt-4 flex cursor-pointer items-center gap-2 text-sm text-slate-700">
                <input
                  type="checkbox"
                  checked={status.enabled}
                  onChange={handleToggle}
                  disabled={actionLoading}
                  className="h-4 w-4 rounded border-slate-300 text-blue-600"
                />
                Enable Weekly Slack Reviews
              </label>
            )}
          </>
        )}
      </div>
    </Layout>
  )
}