<script setup lang="ts">
import type { FatoExecucao, TempoGasto } from '~/types/api'

definePageMeta({
  layout: 'dashboard'
})

const { data: execucoes, status } = await useApi<FatoExecucao[]>('/api/fato/execucao-tarefas')
const { data: tempoGasto } = await useApi<TempoGasto>('/api/dim/tempo-gasto')

const loading = computed(() => status.value === 'pending')

const responsavelMaisProdutivo = computed(() => {
  if (!execucoes.value?.length) return '-'
  const map = new Map<string, number>()
  for (const e of execucoes.value) {
    map.set(e.sk_responsavel, (map.get(e.sk_responsavel) ?? 0) + Number(e.horas_trabalhadas))
  }
  return [...map.entries()].sort((a, b) => b[1] - a[1])[0]?.[0] ?? '-'
})

const mediaPorExecucao = computed(() => {
  if (!execucoes.value?.length) return 0
  const total = execucoes.value.reduce((acc, e) => acc + Number(e.horas_trabalhadas), 0)
  return (total / execucoes.value.length).toFixed(1)
})

const stats = computed(() => [
  {
    label: 'Total de horas registradas',
    value: `${tempoGasto.value?.total_tempo_gasto.toFixed(1) ?? 0}h`,
    icon: 'i-lucide-clock'
  },
  {
    label: 'Responsável mais produtivo',
    value: responsavelMaisProdutivo.value,
    icon: 'i-lucide-user-check'
  },
  {
    label: 'Média de horas por execução',
    value: `${mediaPorExecucao.value}h`,
    icon: 'i-lucide-bar-chart-2'
  }
])
</script>

<template>
  <UDashboardPanel>
    <template #header>
      <UDashboardNavbar
        title="Produtividade"
        icon="i-lucide-activity"
      >
        <template #right>
          <UColorModeButton />
        </template>
      </UDashboardNavbar>
    </template>

    <template #body>
      <div class="space-y-6">
        <div class="grid grid-cols-1 gap-4 sm:grid-cols-3">
          <template v-if="loading">
            <UCard
              v-for="i in 3"
              :key="i"
            >
              <div class="flex items-center justify-between">
                <div class="space-y-2">
                  <USkeleton class="h-4 w-24" />
                  <USkeleton class="h-8 w-20" />
                </div>
                <USkeleton class="size-8 rounded-full" />
              </div>
            </UCard>
          </template>
          <template v-else>
            <UCard
              v-for="stat in stats"
              :key="stat.label"
            >
              <div class="flex items-center justify-between">
                <div>
                  <p class="text-sm text-gray-500">
                    {{ stat.label }}
                  </p>
                  <p class="mt-1 truncate text-xl font-bold">
                    {{ stat.value }}
                  </p>
                </div>
                <UIcon
                  :name="stat.icon"
                  class="size-8 text-primary"
                />
              </div>
            </UCard>
          </template>
        </div>

        <div class="grid grid-cols-1 gap-6 lg:grid-cols-2">
          <UCard>
            <template #header>
              <div class="flex items-center gap-2">
                <UIcon
                  name="i-lucide-bar-chart-horizontal"
                  class="size-5 text-primary"
                />
                <h3 class="font-semibold">
                  Horas por responsável — top 10
                </h3>
              </div>
            </template>
            <template v-if="loading">
              <div class="flex h-80 items-end gap-3 px-4">
                <USkeleton
                  v-for="i in 5"
                  :key="i"
                  class="flex-1 rounded-t"
                  :style="{ height: `${20 + i * 12}%` }"
                />
              </div>
            </template>
            <ProductivityBarChart
              v-if="!loading && execucoes && execucoes.length > 0"
              :execucoes="execucoes"
            />
          </UCard>

          <ProductivityTable
            v-if="execucoes"
            :execucoes="execucoes"
          />
        </div>
      </div>
    </template>
  </UDashboardPanel>
</template>
