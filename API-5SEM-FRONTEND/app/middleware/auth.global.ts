export default defineNuxtRouteMiddleware((to) => {
  const { isLoggedIn, role } = useAuth()

  // Página de login: única rota pública
  if (to.path === '/login') {
    if (isLoggedIn.value) {
      return navigateTo(role.value === 'compras' ? '/pedidos' : '/')
    }
    return
  }

  // Demais rotas exigem autenticação
  if (!isLoggedIn.value) {
    return navigateTo('/login')
  }

  // Perfil "compras" só acessa a tela de Pedidos de Compra
  if (role.value === 'compras' && to.path !== '/pedidos') {
    return navigateTo('/pedidos')
  }
})
