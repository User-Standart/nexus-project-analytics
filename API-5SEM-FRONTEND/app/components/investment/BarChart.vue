<script setup lang="ts">
import { Bar } from 'vue-chartjs'
import { useChartColors } from '~/composables/useChartColors'
import type { ProgramaInvestimento } from '~/types/api'

const props = defineProps<{
  programas: ProgramaInvestimento[]
}>()

const { textColor, gridColor } = useChartColors()

const sorted = computed(() =>
  [...props.programas].sort((a, b) => Number(b.investimento_total) - Number(a.investimento_total))
)

const chartData = computed(() => ({
  labels: sorted.value.map(p => p.nome_programa),
  datasets: [
    {
      label: 'Investimento Total (R$)',
      data: sorted.value.map(p => Number(p.investimento_total)),
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
    },
    tooltip: {
      callbacks: {
        label: (ctx: any) =>
          Number(ctx.raw).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })
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
        callback: (value: any) =>
          Number(value).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })
      },
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
