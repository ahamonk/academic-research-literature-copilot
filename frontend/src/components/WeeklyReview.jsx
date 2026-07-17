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
    <div className="bg-white border border-gray-200 rounded-lg p-5 shadow-sm mb-8">
      <div className="flex justify-between items-center mb-3">
        <h2 className="font-semibold text-gray-800">
          Weekly Literature Review
        </h2>

        <button
          onClick={handleGenerate}
          disabled={loading}
          className="bg-blue-600 hover:bg-blue-700 disabled:bg-blue-300 text-white text-sm font-medium px-4 py-2 rounded-md"
        >
          {loading ? 'Generating...' : 'Generate Review'}
        </button>
      </div>

      {error && (
        <p className="text-red-600 text-sm mb-3">
          {error}
        </p>
      )}

      {loading && (
        <p className="text-sm text-gray-500">
          Fetching papers, summarizing, reviewing, and analyzing trends — this may
          take a moment...
        </p>
      )}

      {!loading && hasGenerated && papers.length === 0 && !error && (
        <p className="text-sm text-gray-500">
          No papers found for your selected research interests yet. Try selecting
          different topics or ingesting more papers.
        </p>
      )}

      {!loading && literatureReview && papers.length > 0 && (
        <>
          <div className="border border-gray-200 rounded-md p-4 mb-4">
            <p className="text-sm text-gray-700 whitespace-pre-wrap leading-relaxed">
              {literatureReview}
            </p>
          </div>

          {references.length > 0 && (
            <div className="mb-6">
              <h3 className="text-sm font-semibold text-gray-700 mb-2">
                References
              </h3>

              <div className="flex flex-col gap-1">
                {references.map((ref) => (
                  <div
                    key={ref.citation}
                    className="text-sm text-gray-600"
                  >
                    [{ref.citation}] {ref.title}{' '}
                    <a
                      href={ref.arxiv_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-blue-600 hover:underline text-xs"
                    >
                      View on arXiv →
                    </a>
                  </div>
                ))}
              </div>
            </div>
          )}

          <details>
            <summary className="text-sm font-medium text-gray-600 cursor-pointer">
              Individual paper summaries ({papers.length})
            </summary>

            <div className="flex flex-col gap-4 mt-3">
              {papers.map((paper, index) => (
                <div
                  key={paper.arxiv_url || index}
                  className="border border-gray-200 rounded-md p-4"
                >
                  <h4 className="font-medium text-gray-800">
                    [{paper.citation}] {paper.title}
                  </h4>

                  <p className="text-xs text-gray-400 mt-1">
                    {paper.primary_category} · {paper.published_date}
                  </p>

                  <p className="text-sm text-gray-700 mt-2">
                    {paper.summary}
                  </p>

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
          </details>
        </>
      )}

      {!loading && !hasGenerated && !error && (
        <p className="text-sm text-gray-500">
          Click "Generate Review" to get an AI-generated weekly literature review
          based on recent papers matching your research interests.
        </p>
      )}
    </div>
  )
}