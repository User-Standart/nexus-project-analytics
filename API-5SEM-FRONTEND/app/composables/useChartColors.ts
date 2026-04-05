export function useChartColors() {
  const colorMode = useColorMode()

  const textColor = computed(() => colorMode.value === 'dark' ? '#a1a1aa' : '#52525b')
  const gridColor = computed(() => colorMode.value === 'dark' ? '#27272a' : '#e4e4e7')

  return { textColor, gridColor }
}
