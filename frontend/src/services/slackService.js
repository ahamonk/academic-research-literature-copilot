import api from './api'

export async function getSlackStatus() {
  const response = await api.get('/slack/status')
  return response.data
}

export async function getSlackConnectUrl() {
  const response = await api.get('/slack/connect')
  return response.data.authorize_url
}

export async function disconnectSlack() {
  const response = await api.post('/slack/disconnect')
  return response.data
}

export async function toggleSlack(enabled) {
  const response = await api.post('/slack/toggle', { enabled })
  return response.data
}