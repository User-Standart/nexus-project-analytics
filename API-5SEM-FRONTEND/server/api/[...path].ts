export default defineEventHandler((event) => {
  const backendUrl = process.env.BACKEND_PATH || 'http://localhost:8080'
  const target = `${backendUrl}${event.path}`

  // Converte o cookie de sessão em header Authorization para o backend.
  const token = getCookie(event, 'auth_token')

  return proxyRequest(event, target, {
    headers: token ? { Authorization: `Bearer ${token}` } : undefined
  })
})
