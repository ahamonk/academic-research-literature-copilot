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
      <h1 className="text-2xl font-semibold text-gray-800 mb-1">Research Interests</h1>
      <p className="text-gray-500 mb-8">
        Choose the topics you want papers and weekly reviews for.
      </p>

      {loading && <p className="text-sm text-gray-500">Loading topics...</p>}
      {error && <p className="text-red-600 text-sm mb-4">{error}</p>}

      {!loading && (
        <div className="bg-white border border-gray-200 rounded-lg p-5 shadow-sm">
          {Object.entries(groupedTopics).map(([discipline, disciplineTopics]) => (
            <div key={discipline} className="mb-6">
              <h2 className="text-sm font-semibold text-gray-700 mb-3 border-b border-gray-200 pb-1">
                {discipline}
              </h2>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                {disciplineTopics.map((topic) => (
                  <label
                    key={topic.id}
                    className="flex items-center gap-2 text-sm text-gray-700 border border-gray-200 rounded-md px-3 py-2 cursor-pointer hover:bg-gray-50"
                  >
                    <input
                      type="checkbox"
                      checked={selectedIds.includes(topic.id)}
                      onChange={() => toggleTopic(topic.id)}
                      className="h-4 w-4"
                    />
                    <span>
                      {topic.name}{' '}
                      <span className="text-gray-400 text-xs">({topic.code})</span>
                    </span>
                  </label>
                ))}
              </div>
            </div>
          ))}

          {message && <p className="text-green-600 text-sm mb-3 mt-2">{message}</p>}

          <button
            onClick={handleSave}
            disabled={saving}
            className="bg-blue-600 hover:bg-blue-700 disabled:bg-blue-300 text-white text-sm font-medium px-4 py-2 rounded-md"
          >
            {saving ? 'Saving...' : 'Save'}
          </button>
        </div>
      )}
    </Layout>
  )
}