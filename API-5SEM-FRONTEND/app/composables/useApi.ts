export function useApi<T>(path: string) {
  // No SSR, encaminha o cookie da requisição para que o proxy injete o token.
  const headers = import.meta.server ? useRequestHeaders(['cookie']) : undefined

  return useAsyncData<T>(
    path,
    () => $fetch<T>(path, { headers }),
    { lazy: true }
  )
}
