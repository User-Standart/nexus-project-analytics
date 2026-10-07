<script setup lang="ts">
import { Bar } from 'vue-chartjs'
import { useChartColors } from '~/composables/useChartColors'
import { statusCounts } from '~/utils/purchases'
import type { Purchase } from '~/types/api'

const props = defineProps<{
  pedidos: Purchase[]
}>()

const { textColor, gridColor } = useChartColors()

const contagem = computed(() => statusCounts(props.pedidos))

const chartData = computed(() => ({
  labels: contagem.value.map(s => s.status),
  datasets: [
    {
      label: 'Pedidos por status',
      data: contagem.value.map(s => s.count),
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
      ticks: { color: textColor.value, precision: 0 },
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
