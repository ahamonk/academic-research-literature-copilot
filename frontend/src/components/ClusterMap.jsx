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
    <div className="bg-white border border-gray-200 rounded-md shadow-sm px-3 py-2 text-xs max-w-xs">
      <p className="font-medium text-gray-800">{point.title}</p>
      <p className="text-gray-500 mt-1">
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
    <div className="bg-white border border-gray-200 rounded-lg p-5 shadow-sm mb-8">
      <h2 className="font-semibold text-gray-800 mb-3">Topic Cluster Map</h2>

      {loading && <p className="text-sm text-gray-500">Loading clusters...</p>}
      {error && <p className="text-red-600 text-sm">{error}</p>}

      {!loading && !error && papers.length === 0 && (
        <p className="text-sm text-gray-500">
          No papers available to cluster yet. Ingest some papers first.
        </p>
      )}

      {!loading && papers.length > 0 && (
        <>
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

          {selectedPaper && (
            <div className="mt-4 border border-gray-200 rounded-md p-4 relative">
              <button
                onClick={() => setSelectedPaper(null)}
                className="absolute top-3 right-3 text-gray-400 hover:text-gray-600 text-sm"
              >
                ✕
              </button>

              <h3 className="font-medium text-gray-800 pr-6">
                {selectedPaper.title}
              </h3>

              <p className="text-xs text-gray-500 mt-1">
                {selectedPaper.authors}
              </p>

              <p className="text-xs text-gray-400 mt-1">
                {selectedPaper.primary_category} · {selectedPaper.published_date} · Cluster{' '}
                {selectedPaper.cluster_id === -1 ? 'Noise' : selectedPaper.cluster_id}
              </p>

              <p className="text-sm text-gray-600 mt-2">
                {selectedPaper.abstract}
              </p>

              <a
                href={selectedPaper.arxiv_url}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-block text-xs text-blue-600 hover:underline mt-2"
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