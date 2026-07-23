import { useState } from 'react'
import Layout from '../components/Layout'
import { useAuth } from '../context/AuthContext'
import api from '../services/api'
import ClusterMap from '../components/ClusterMap'
import WeeklyReview from '../components/WeeklyReview'

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

  return (
    <Layout>
      <section className="mb-8 rounded-2xl border border-slate-200 bg-white p-6 shadow-sm sm:p-8">
        <div className="flex flex-col gap-3 md:flex-row md:items-end md:justify-between">
          <div>
            <p className="text-sm font-medium text-blue-600">Research workspace</p>
            <h1 className="mt-1 text-3xl font-semibold tracking-tight text-slate-900">
              Welcome{user?.full_name ? `, ${user.full_name}` : ''}
            </h1>
            <p className="mt-2 text-sm leading-6 text-slate-600">
              Here is a focused overview of your research copilot.
            </p>
          </div>
          <div className="rounded-full border border-slate-200 bg-slate-50 px-3 py-1.5 text-sm text-slate-600">
            Semantic search and review insights
          </div>
        </div>
      </section>

      <section className="mb-8 rounded-2xl border border-slate-200 bg-white p-6 shadow-sm sm:p-8">
        <div className="mb-5 flex flex-col gap-2 sm:flex-row sm:items-end sm:justify-between">
          <div>
            <h2 className="text-lg font-semibold text-slate-900">Semantic Search</h2>
            <p className="text-sm text-slate-600">
              Search papers by meaning, not just keywords.
            </p>
          </div>
        </div>

        <form onSubmit={handleSearch} className="mb-5 flex flex-col gap-3 sm:flex-row">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search papers by meaning, not just keywords..."
            className="flex-1 rounded-xl border border-slate-300 bg-slate-50 px-4 py-3 text-sm text-slate-900 outline-none transition focus:border-blue-500 focus:bg-white focus:ring-2 focus:ring-blue-100"
          />

          <button
            type="submit"
            disabled={loading}
            className="rounded-xl bg-blue-600 px-4 py-3 text-sm font-medium text-white transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:bg-blue-300"
          >
            {loading ? 'Searching...' : 'Search'}
          </button>
        </form>

        {error && (
          <div className="mb-4 rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
            {error}
          </div>
        )}

        {hasSearched && !loading && results.length === 0 && !error && (
          <div className="rounded-xl border border-dashed border-slate-300 bg-slate-50 px-4 py-6 text-sm text-slate-500">
            No matching papers found.
          </div>
        )}

        {results.length > 0 && (
          <div className="flex max-h-[520px] flex-col gap-3 overflow-y-auto pr-1">
            {results.map((paper) => (
              <div
                key={paper.arxiv_id}
                className="rounded-xl border border-slate-200 bg-slate-50 p-4 transition-shadow hover:shadow-sm"
              >
                <div className="flex flex-col gap-2 sm:flex-row sm:items-start sm:justify-between">
                  <h3 className="text-sm font-semibold text-slate-900">
                    {paper.title}
                  </h3>

                  <span className="whitespace-nowrap text-xs font-medium text-blue-600">
                    {(paper.similarity_score * 100).toFixed(1)}% match
                  </span>
                </div>

                <p className="mt-2 text-xs text-slate-500">
                  {paper.authors}
                </p>

                <p className="mt-1 text-xs text-slate-400">
                  {paper.primary_category} · {paper.published_date}
                </p>

                <p className="mt-3 text-sm leading-6 text-slate-600">
                  {paper.abstract}
                </p>

                <a
                  href={paper.arxiv_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="mt-3 inline-flex text-xs font-medium text-blue-600 transition hover:text-blue-700"
                >
                  View on arXiv →
                </a>
              </div>
            ))}
          </div>
        )}
      </section>

      <ClusterMap />

      <WeeklyReview />

    </Layout>
  )
}