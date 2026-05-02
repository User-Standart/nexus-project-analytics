export function useApi<T>(path: string) {
  return useAsyncData<T>(
    path,
    () => $fetch<T>(path),
    { lazy: true }
  )
}
