import { useEffect, useState } from 'react'
import {
  ScatterChart,
  Scatter,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Cell,
} from 'recharts'
import { fetchClusters } from '../services/clustersService'

const COLORS = [
  '#2563eb', '#dc2626', '#059669', '#d97706', '#7c3aed',
  '#db2777', '#0891b2', '#65a30d', '#ea580c', '#4f46e5',
]

function colorForCluster(clusterId) {
  if (clusterId === -1) return '#9ca3af'
  return COLORS[clusterId % COLORS.length]
}

function ClusterTooltip({ active, payload }) {
  if (!active || !payload || !payload.length) return null
  const point = payload[0].payload
  return (
    <div className="max-w-xs rounded-xl border border-slate-200 bg-white px-3 py-2 text-xs shadow-sm">
      <p className="font-medium text-slate-800">{point.title}</p>
      <p className="mt-1 text-slate-500">
        {point.primary_category} · Cluster {point.cluster_id === -1 ? 'Noise' : point.cluster_id}
      </p>
    </div>
  )
}

export default function ClusterMap() {
  const [papers, setPapers] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [selectedPaper, setSelectedPaper] = useState(null)

  useEffect(() => {
    loadClusters()
  }, [])

  const loadClusters = async () => {
    setLoading(true)
    setError('')
    try {
      const data = await fetchClusters()
      setPapers(data)
    } catch {
      setError('Failed to load cluster data.')
    } finally {
      setLoading(false)
    }
  }

  const handlePointClick = (data) => {
    setSelectedPaper(data?.payload ?? data)
  }

  return (
    <div className="mb-8 rounded-2xl border border-slate-200 bg-white p-6 shadow-sm sm:p-8">
      <div className="mb-5">
        <h2 className="text-lg font-semibold text-slate-900">Topic Cluster Map</h2>
        <p className="mt-1 text-sm text-slate-600">
          Visualize how recent papers group into related research areas.
        </p>
      </div>

      {loading && (
        <div className="rounded-xl border border-slate-200 bg-slate-50 px-4 py-6 text-sm text-slate-500">
          Loading clusters...
        </div>
      )}
      {error && (
        <div className="rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
          {error}
        </div>
      )}

      {!loading && !error && papers.length === 0 && (
        <div className="rounded-xl border border-dashed border-slate-300 bg-slate-50 px-4 py-6 text-sm text-slate-500">
          No papers available to cluster yet. Ingest some papers first.
        </div>
      )}

      {!loading && papers.length > 0 && (
        <>
          <div className="rounded-xl border border-slate-200 bg-slate-50 p-2">
            <ResponsiveContainer width="100%" height={400}>
              <ScatterChart margin={{ top: 10, right: 10, bottom: 10, left: 10 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                <XAxis type="number" dataKey="x" name="x" tick={false} axisLine={false} />
                <YAxis type="number" dataKey="y" name="y" tick={false} axisLine={false} />
                <Tooltip content={<ClusterTooltip />} cursor={{ strokeDasharray: '3 3' }} />
                <Scatter data={papers} onClick={handlePointClick} cursor="pointer">
                  {papers.map((point, index) => (
                    <Cell
                      key={point.arxiv_id || index}
                      fill={colorForCluster(point.cluster_id)}
                    />
                  ))}
                </Scatter>
              </ScatterChart>
            </ResponsiveContainer>
          </div>

          {selectedPaper && (
            <div className="relative mt-4 rounded-xl border border-slate-200 bg-white p-4">
              <button
                onClick={() => setSelectedPaper(null)}
                className="absolute right-3 top-3 text-sm text-slate-400 transition hover:text-slate-600"
              >
                ✕
              </button>

              <h3 className="pr-6 text-sm font-semibold text-slate-900">
                {selectedPaper.title}
              </h3>

              <p className="mt-2 text-xs text-slate-500">
                {selectedPaper.authors}
              </p>

              <p className="mt-1 text-xs text-slate-400">
                {selectedPaper.primary_category} · {selectedPaper.published_date} · Cluster{' '}
                {selectedPaper.cluster_id === -1 ? 'Noise' : selectedPaper.cluster_id}
              </p>

              <p className="mt-3 text-sm leading-6 text-slate-600">
                {selectedPaper.abstract}
              </p>

              <a
                href={selectedPaper.arxiv_url}
                target="_blank"
                rel="noopener noreferrer"
                className="mt-3 inline-flex text-xs font-medium text-blue-600 transition hover:text-blue-700"
              >
                View on arXiv →
              </a>
            </div>
          )}
        </>
      )}
    </div>
  )
}