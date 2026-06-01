interface AuthUser {
  nome: string
  role: string
}

interface LoginResponse {
  token: string
  usuario: AuthUser
}

const COOKIE_MAX_AGE = 60 * 60 * 8 // 8h, alinhado ao JWT_EXPIRY do backend

export function useAuth() {
  const token = useCookie<string | null>('auth_token', {
    maxAge: COOKIE_MAX_AGE,
    sameSite: 'lax'
  })
  const user = useCookie<AuthUser | null>('auth_user', {
    maxAge: COOKIE_MAX_AGE,
    sameSite: 'lax'
  })

  const isLoggedIn = computed(() => !!token.value)
  const role = computed(() => user.value?.role ?? null)

  async function login(email: string, senha: string) {
    const res = await $fetch<LoginResponse>('/api/auth/login', {
      method: 'POST',
      body: { email, senha }
    })
    token.value = res.token
    user.value = res.usuario
    return res
  }

  async function logout() {
    try {
      await $fetch('/api/auth/logout', { method: 'POST' })
    } catch {
      // ignora erro de rede: limpamos a sessão local de qualquer forma
    }
    token.value = null
    user.value = null
    await navigateTo('/login')
  }

  return { token, user, isLoggedIn, role, login, logout }
}
