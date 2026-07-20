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
      <h1 className="text-2xl font-semibold text-gray-800 mb-1">Settings</h1>
      <p className="text-gray-500 mb-8">Manage integrations for your account.</p>

      <div className="bg-white border border-gray-200 rounded-lg p-5 shadow-sm max-w-lg">
        <h2 className="font-semibold text-gray-800 mb-3">Slack</h2>

        {loading && <p className="text-sm text-gray-500">Loading...</p>}
        {error && <p className="text-red-600 text-sm mb-3">{error}</p>}

        {!loading && (
          <>
            <div className="flex items-center justify-between mb-4">
              <div>
                <p className="text-sm text-gray-700">
                  Status:{' '}
                  <span className={status.connected ? 'text-green-600 font-medium' : 'text-gray-500'}>
                    {status.connected ? 'Connected' : 'Not Connected'}
                  </span>
                </p>
                {status.connected && status.workspace_name && (
                  <p className="text-xs text-gray-400 mt-1">Workspace: {status.workspace_name}</p>
                )}
              </div>

              {status.connected ? (
                <button
                  onClick={handleDisconnect}
                  disabled={actionLoading}
                  className="text-sm px-3 py-1.5 rounded-md bg-gray-100 hover:bg-gray-200 text-gray-700 disabled:opacity-50"
                >
                  Disconnect Slack
                </button>
              ) : (
                <button
                  onClick={handleConnect}
                  disabled={actionLoading}
                  className="text-sm px-3 py-1.5 rounded-md bg-blue-600 hover:bg-blue-700 text-white disabled:opacity-50"
                >
                  Connect Slack
                </button>
              )}
            </div>

            {status.connected && (
              <label className="flex items-center gap-2 text-sm text-gray-700 cursor-pointer">
                <input
                  type="checkbox"
                  checked={status.enabled}
                  onChange={handleToggle}
                  disabled={actionLoading}
                  className="h-4 w-4"
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