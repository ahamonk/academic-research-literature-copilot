import api from './api'

export async function fetchClusters() {
  const response = await api.get('/clusters')
  return response.data
}