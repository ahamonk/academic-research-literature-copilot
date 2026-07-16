import api from './api'

export async function fetchAllTopics() {
  const response = await api.get('/topics')
  return response.data
}

export async function fetchMyTopics() {
  const response = await api.get('/topics/my')
  return response.data
}

export async function saveMyTopics(topicIds) {
  const response = await api.post('/topics/select', { topic_ids: topicIds })
  return response.data
}