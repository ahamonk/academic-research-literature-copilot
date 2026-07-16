import api from './api'

export async function generateReview() {
  const response = await api.post('/review/generate')
  return response.data
}