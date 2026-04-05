<script setup lang="ts">
import { Line } from 'vue-chartjs'
import { useChartColors } from '~/composables/useChartColors'

const props = defineProps<{
  labels: string[]
  data: number[]
  label?: string
}>()

const { textColor, gridColor } = useChartColors()

const chartData = computed(() => ({
  labels: props.labels,
  datasets: [
    {
      label: props.label ?? 'Valor',
      data: props.data,
      borderColor: '#EA3837',
      backgroundColor: 'rgba(234, 56, 55, 0.1)',
      fill: true,
      tension: 0.4,
      pointRadius: 4,
      pointHoverRadius: 6
    }
  ]
}))

const options = computed(() => ({
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
      ticks: { color: textColor.value },
      grid: { color: gridColor.value }
    }
  }
}))
</script>

<template>
  <div class="h-72 w-full">
    <Line
      :data="chartData"
      :options="options"
    />
  </div>
</template>
