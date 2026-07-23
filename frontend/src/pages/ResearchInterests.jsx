import { useEffect, useState } from 'react'
import Layout from '../components/Layout'
import { fetchAllTopics, fetchMyTopics, saveMyTopics } from '../services/topicsService'

export default function ResearchInterests() {
  const [topics, setTopics] = useState([])
  const [selectedIds, setSelectedIds] = useState([])
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')

  useEffect(() => {
    loadData()
  }, [])

  const loadData = async () => {
    setLoading(true)
    setError('')
    try {
      const [allTopics, myTopics] = await Promise.all([fetchAllTopics(), fetchMyTopics()])
      setTopics(allTopics)
      setSelectedIds(myTopics.map((t) => t.id))
    } catch {
      setError('Failed to load topics.')
    } finally {
      setLoading(false)
    }
  }

  const toggleTopic = (id) => {
    setSelectedIds((prev) =>
      prev.includes(id) ? prev.filter((tid) => tid !== id) : [...prev, id]
    )
    setMessage('')
  }

  const handleSave = async () => {
    setSaving(true)
    setMessage('')
    setError('')
    try {
      await saveMyTopics(selectedIds)
      setMessage('Research interests updated successfully.')
    } catch {
      setError('Failed to save your selections.')
    } finally {
      setSaving(false)
    }
  }

  const groupedTopics = topics.reduce((groups, topic) => {
    const discipline = topic.discipline || 'Other'
    if (!groups[discipline]) groups[discipline] = []
    groups[discipline].push(topic)
    return groups
  }, {})

  return (
    <Layout>
      <section className="mb-6 rounded-2xl border border-slate-200 bg-white p-6 shadow-sm sm:p-8">
        <div className="flex flex-col gap-3 md:flex-row md:items-end md:justify-between">
          <div>
            <h1 className="text-2xl font-semibold tracking-tight text-slate-900">Research Interests</h1>
            <p className="mt-2 text-sm leading-6 text-slate-600">
              Choose the topics you want papers and weekly reviews for.
            </p>
          </div>
          <div className="rounded-full border border-slate-200 bg-slate-50 px-3 py-1.5 text-sm text-slate-600">
            {selectedIds.length} selected
          </div>
        </div>
      </section>

      {loading && (
        <div className="rounded-2xl border border-slate-200 bg-white p-6 text-sm text-slate-500 shadow-sm">
          Loading topics...
        </div>
      )}
      {error && (
        <div className="mb-4 rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
          {error}
        </div>
      )}

      {!loading && (
        <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm sm:p-8">
          {Object.entries(groupedTopics).map(([discipline, disciplineTopics]) => (
            <div key={discipline} className="mb-6">
              <h2 className="mb-3 border-b border-slate-200 pb-2 text-sm font-semibold uppercase tracking-[0.2em] text-slate-500">
                {discipline}
              </h2>
              <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
                {disciplineTopics.map((topic) => (
                  <label
                    key={topic.id}
                    className="flex cursor-pointer items-start gap-3 rounded-xl border border-slate-200 px-3 py-3 text-sm text-slate-700 transition hover:border-blue-200 hover:bg-slate-50"
                  >
                    <input
                      type="checkbox"
                      checked={selectedIds.includes(topic.id)}
                      onChange={() => toggleTopic(topic.id)}
                      className="mt-1 h-4 w-4 rounded border-slate-300 text-blue-600"
                    />
                    <span>
                      {topic.name}{' '}
                      <span className="text-xs text-slate-400">({topic.code})</span>
                    </span>
                  </label>
                ))}
              </div>
            </div>
          ))}

          {message && (
            <div className="mb-4 rounded-xl border border-emerald-200 bg-emerald-50 px-4 py-3 text-sm text-emerald-700">
              {message}
            </div>
          )}

          <button
            onClick={handleSave}
            disabled={saving}
            className="rounded-xl bg-blue-600 px-4 py-2.5 text-sm font-medium text-white transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:bg-blue-300"
          >
            {saving ? 'Saving...' : 'Save'}
          </button>
        </div>
      )}
    </Layout>
  )
}