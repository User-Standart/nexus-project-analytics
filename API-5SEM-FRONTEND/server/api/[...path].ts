export default defineEventHandler((event) => {
  const backendUrl = process.env.BACKEND_PATH || 'http://localhost:8080'
  const target = `${backendUrl}${event.path}`
  return proxyRequest(event, target)
})
