import { useState } from 'react'
import { generateReview } from '../services/reviewService'

export default function WeeklyReview() {
  const [literatureReview, setLiteratureReview] = useState('')
  const [references, setReferences] = useState([])
  const [papers, setPapers] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [hasGenerated, setHasGenerated] = useState(false)

  const handleGenerate = async () => {
    setLoading(true)
    setError('')

    try {
      const data = await generateReview()
      setLiteratureReview(data.literature_review)
      setReferences(data.references)
      setPapers(data.papers)
      setHasGenerated(true)
    } catch (err) {
      const detail = err.response?.data?.detail
      setError(detail || 'Failed to generate the literature review. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="mb-8 rounded-2xl border border-slate-200 bg-white p-6 shadow-sm sm:p-8">
      <div className="mb-5 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h2 className="text-lg font-semibold text-slate-900">Weekly Literature Review</h2>
          <p className="mt-1 text-sm text-slate-600">
            Generate a concise synthesis of recent papers for your interests.
          </p>
        </div>

        <button
          onClick={handleGenerate}
          disabled={loading}
          className="rounded-xl bg-blue-600 px-4 py-2.5 text-sm font-medium text-white transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:bg-blue-300"
        >
          {loading ? 'Generating...' : 'Generate Review'}
        </button>
      </div>

      {error && (
        <div className="mb-4 rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
          {error}
        </div>
      )}

      {loading && (
        <div className="rounded-xl border border-slate-200 bg-slate-50 px-4 py-6 text-sm text-slate-500">
          Fetching papers, summarizing, reviewing, and analyzing trends — this may take a moment...
        </div>
      )}

      {!loading && hasGenerated && papers.length === 0 && !error && (
        <div className="rounded-xl border border-dashed border-slate-300 bg-slate-50 px-4 py-6 text-sm text-slate-500">
          No papers found for your selected research interests yet. Try selecting different topics or ingesting more papers.
        </div>
      )}

      {!loading && literatureReview && papers.length > 0 && (
        <>
          <div className="mb-6 rounded-xl border border-slate-200 bg-slate-50 p-4">
            <p className="whitespace-pre-wrap text-sm leading-7 text-slate-700">
              {literatureReview}
            </p>
          </div>

          {references.length > 0 && (
            <div className="mb-6">
              <h3 className="mb-2 text-sm font-semibold uppercase tracking-[0.2em] text-slate-500">
                References
              </h3>

              <div className="flex flex-col gap-2">
                {references.map((ref) => (
                  <div
                    key={ref.citation}
                    className="rounded-lg border border-slate-200 bg-white px-3 py-3 text-sm text-slate-600"
                  >
                    [{ref.citation}] {ref.title}{' '}
                    <a
                      href={ref.arxiv_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="ml-1 text-xs font-medium text-blue-600 transition hover:text-blue-700"
                    >
                      View on arXiv →
                    </a>
                  </div>
                ))}
              </div>
            </div>
          )}

          <details className="rounded-xl border border-slate-200 bg-white p-4">
            <summary className="cursor-pointer text-sm font-medium text-slate-700">
              Individual paper summaries ({papers.length})
            </summary>

            <div className="mt-4 flex flex-col gap-4">
              {papers.map((paper, index) => (
                <div
                  key={paper.arxiv_url || index}
                  className="rounded-xl border border-slate-200 bg-slate-50 p-4"
                >
                  <h4 className="text-sm font-semibold text-slate-900">
                    [{paper.citation}] {paper.title}
                  </h4>

                  <p className="mt-1 text-xs text-slate-400">
                    {paper.primary_category} · {paper.published_date}
                  </p>

                  <p className="mt-3 text-sm leading-7 text-slate-700">
                    {paper.summary}
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
          </details>
        </>
      )}

      {!loading && !hasGenerated && !error && (
        <div className="rounded-xl border border-dashed border-slate-300 bg-slate-50 px-4 py-6 text-sm text-slate-500">
          Click "Generate Review" to get an AI-generated weekly literature review based on recent papers matching your research interests.
        </div>
      )}
    </div>
  )
}