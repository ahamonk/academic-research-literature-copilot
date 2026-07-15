import { useState } from 'react'
import Layout from '../components/Layout'
import { useAuth } from '../context/AuthContext'
import api from '../services/api'

export default function Dashboard() {
  const { user } = useAuth()

  const [query, setQuery] = useState('')
  const [results, setResults] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [hasSearched, setHasSearched] = useState(false)

  const handleSearch = async (e) => {
    e.preventDefault()
    if (!query.trim()) return

    setLoading(true)
    setError('')
    try {
      const response = await api.post('/search', { query, top_k: 10 })
      setResults(response.data.results)
      setHasSearched(true)
    } catch {
      setError('Search failed. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const cards = [
    {
      title: 'Paper Library',
      description: 'Browse papers ingested from arXiv for your subscribed topics.',
    },
    {
      title: 'Weekly Literature Review',
      description: 'Read the latest AI-generated review for each topic you follow.',
    },
    {
      title: 'Topic Cluster Map',
      description: 'Visualize how recent papers cluster by theme and similarity.',
    },
  ]

  return (
    <Layout>
      <h1 className="text-2xl font-semibold text-gray-800 mb-1">
        Welcome{user?.full_name ? `, ${user.full_name}` : ''}
      </h1>
      <p className="text-gray-500 mb-8">Here's an overview of your research copilot.</p>

      <div className="bg-white border border-gray-200 rounded-lg p-5 shadow-sm mb-8">
        <h2 className="font-semibold text-gray-800 mb-3">Semantic Search</h2>

        <form onSubmit={handleSearch} className="flex gap-2 mb-4">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search papers by meaning, not just keywords..."
            className="flex-1 border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button
            type="submit"
            disabled={loading}
            className="bg-blue-600 hover:bg-blue-700 disabled:bg-blue-300 text-white text-sm font-medium px-4 py-2 rounded-md"
          >
            {loading ? 'Searching...' : 'Search'}
          </button>
        </form>

        {error && <p className="text-red-600 text-sm mb-4">{error}</p>}

        {hasSearched && !loading && results.length === 0 && !error && (
          <p className="text-sm text-gray-500">No matching papers found.</p>
        )}

        {results.length > 0 && (
          <div className="max-h-[500px] overflow-y-auto flex flex-col gap-3">
            {results.map((paper) => (
              <div
                key={paper.arxiv_id}
                className="border border-gray-200 rounded-md p-4"
              >
                <div className="flex justify-between items-start gap-3">
                  <h3 className="font-medium text-gray-800">{paper.title}</h3>
                  <span className="text-xs text-gray-400 whitespace-nowrap">
                    {(paper.similarity_score * 100).toFixed(1)}% match
                  </span>
                </div>

                <p className="text-xs text-gray-500 mt-1">{paper.authors}</p>

                <p className="text-xs text-gray-400 mt-1">
                  {paper.primary_category} · {paper.published_date}
                </p>

                <p className="text-sm text-gray-600 mt-2">{paper.abstract}</p>

                <a
                  href={paper.arxiv_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-block text-xs text-blue-600 hover:underline mt-2"
                >
                  View on arXiv →
                </a>
              </div>
            ))}
          </div>
        )}
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        {cards.map((card) => (
          <div
            key={card.title}
            className="bg-white border border-gray-200 rounded-lg p-5 shadow-sm"
          >
            <h2 className="font-semibold text-gray-800 mb-2">{card.title}</h2>
            <p className="text-sm text-gray-500">{card.description}</p>
            <span className="inline-block mt-4 text-xs text-gray-400">Coming soon</span>
          </div>
        ))}
      </div>
    </Layout>
  )
}