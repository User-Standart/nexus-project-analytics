<script setup lang="ts">
import { Bar } from 'vue-chartjs'
import { useChartColors } from '~/composables/useChartColors'
import type { MateriaisPorProjeto } from '~/types/api'

const props = defineProps<{
  materiais: MateriaisPorProjeto[]
}>()

const { textColor, gridColor } = useChartColors()

const agrupado = computed(() => {
  const map = new Map<string, number>()
  for (const m of props.materiais) {
    map.set(m.nome_projeto, (map.get(m.nome_projeto) ?? 0) + m.quantidade_estoque)
  }
  return [...map.entries()]
    .sort((a, b) => b[1] - a[1])
    .slice(0, 10)
})

const chartData = computed(() => ({
  labels: agrupado.value.map(([nome]) => nome),
  datasets: [
    {
      label: 'Quantidade em estoque',
      data: agrupado.value.map(([, qtd]) => qtd),
      backgroundColor: '#EA3837',
      borderRadius: 6
    }
  ]
}))

const options = computed(() => ({
  indexAxis: 'y' as const,
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      labels: {
        color: textColor.value,
        usePointStyle: true,
        pointStyle: 'circle'
      }
    }
  },
  scales: {
    x: {
      ticks: { color: textColor.value },
      grid: { color: gridColor.value }
    },
    y: {
      ticks: {
        color: textColor.value,
        font: { size: 11 }
      },
      grid: { color: gridColor.value }
    }
  }
}))
</script>

<template>
  <div class="h-80 w-full">
    <Bar
      :data="chartData"
      :options="options"
    />
  </div>
</template>
