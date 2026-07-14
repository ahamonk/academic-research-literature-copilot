import Layout from '../components/Layout'
import { useAuth } from '../context/AuthContext'

export default function Dashboard() {
  const { user } = useAuth()

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