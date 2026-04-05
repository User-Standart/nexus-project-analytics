<script setup lang="ts">
import { Bar } from 'vue-chartjs'
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
      backgroundColor: '#EA3837',
      borderRadius: 6
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
    <Bar
      :data="chartData"
      :options="options"
    />
  </div>
</template>
