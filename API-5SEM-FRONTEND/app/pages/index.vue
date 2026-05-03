<script setup lang="ts">
import type { DimProjeto, DimTarefa, FatoExecucao, FatoCompra } from '~/types/api'

definePageMeta({
  layout: 'dashboard'
})

const { data: projetos, status: projetosStatus } = useApi<DimProjeto[]>('/api/dim/projetos')
const { data: tarefas, status: tarefasStatus } = useApi<DimTarefa[]>('/api/dim/tarefas')
const { data: execucoes, status: execucoesStatus } = useApi<FatoExecucao[]>('/api/fato/execucao-tarefas')
const { data: compras, status: comprasStatus } = useApi<FatoCompra[]>('/api/fato/compras')

const loading = computed(() =>
  projetosStatus.value !== 'success'
  || tarefasStatus.value !== 'success'
  || execucoesStatus.value !== 'success'
  || comprasStatus.value !== 'success'
)

const filtros = ref({ programa: 'Todos', status: 'Todos' })

const filterFields = computed(() => [
  {
    key: 'programa' as const,
    label: 'Programa',
    options: ['Todos', ...new Set(projetos.value?.map(p => p.nome_programa) ?? [])]
  },
  {
    key: 'status' as const,
    label: 'Status',
    options: ['Todos', ...new Set(projetos.value?.map(p => p.status) ?? [])]
  }
])

const projetosFiltrados = computed(() => {
  if (!projetos.value) return []
  return projetos.value.filter(p =>
    (filtros.value.programa === 'Todos' || p.nome_programa === filtros.value.programa)
    && (filtros.value.status === 'Todos' || p.status === filtros.value.status)
  )
})

const skProjetosFiltrados = computed(() => new Set(projetosFiltrados.value.map(p => p.id_projeto)))

const execucoesFiltradas = computed(() =>
  execucoes.value?.filter(e => skProjetosFiltrados.value.has(e.sk_projeto)) ?? []
)

const comprasFiltradas = computed(() =>
  compras.value?.filter(c => skProjetosFiltrados.value.has(c.sk_projeto)) ?? []
)

const totalHoras = computed(() =>
  execucoesFiltradas.value.reduce((acc, e) => acc + Number(e.horas_trabalhadas), 0)
)

const totalCompras = computed(() =>
  comprasFiltradas.value.reduce((acc, c) => acc + Number(c.valor_total_pedido), 0)
)

const stats = computed(() => [
  {
    label: 'Projetos',
    value: projetosFiltrados.value.length,
    icon: 'i-lucide-folder-kanban'
  },
  {
    label: 'Tarefas',
    value: tarefas.value?.length ?? 0,
    icon: 'i-lucide-list-checks'
  },
  {
    label: 'Horas Trabalhadas',
    value: `${totalHoras.value.toFixed(1)}h`,
    icon: 'i-lucide-clock'
  },
  {
    label: 'Valor em Compras',
    value: totalCompras.value.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' }),
    icon: 'i-lucide-shopping-cart'
  }
])

const projetoNomeMap = computed(() => {
  if (!projetosFiltrados.value.length) return new Map<string, string>()
  return new Map(projetosFiltrados.value.map(p => [p.id_projeto, p.nome_projeto]))
})

function groupBy(items: { sk_projeto: string }[] | null, field: string) {
  if (!items) return { labels: [], data: [] }

  const map = new Map<string, number>()
  for (const item of items) {
    const key = item.sk_projeto
    const val = Number((item as Record<string, string>)[field])
    map.set(key, (map.get(key) ?? 0) + val)
  }

  const labels: string[] = []
  const data: number[] = []
  for (const [sk, total] of map) {
    labels.push(projetoNomeMap.value.get(sk) ?? `Projeto ${sk}`)
    data.push(total)
  }
  return { labels, data }
}

const horasPorProjeto = computed(() => groupBy(execucoesFiltradas.value, 'horas_trabalhadas'))
const comprasPorProjeto = computed(() => groupBy(comprasFiltradas.value, 'valor_alocado_projeto'))
</script>

<template>
  <UDashboardPanel>
    <template #header>
      <UDashboardNavbar
        title="Home"
        icon="i-lucide-house"
      >
        <template #right>
          <UColorModeButton />
        </template>
      </UDashboardNavbar>
    </template>

    <template #body>
      <AppFilters
        v-if="!loading"
        v-model="filtros"
        :fields="filterFields"
        class="mb-4"
      />

      <div class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <template v-if="loading">
          <UCard
            v-for="i in 4"
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
          <HomeStatCard
            v-for="stat in stats"
            :key="stat.label"
            :label="stat.label"
            :value="stat.value"
            :icon="stat.icon"
          />
        </template>
      </div>

      <div class="mt-6 grid grid-cols-1 gap-6 lg:grid-cols-2">
        <UCard>
          <template #header>
            <div class="flex items-center gap-2">
              <UIcon
                name="i-lucide-bar-chart-3"
                class="size-5 text-primary"
              />
              <h3 class="font-semibold">
                Horas Trabalhadas por Projeto
              </h3>
            </div>
          </template>
          <template v-if="loading">
            <div class="flex h-72 items-end gap-3 px-4">
              <USkeleton
                v-for="i in 5"
                :key="i"
                class="flex-1 rounded-t"
                :style="{ height: `${20 + i * 12}%` }"
              />
            </div>
          </template>
          <HomeBarChart
            v-else
            :labels="horasPorProjeto.labels"
            :data="horasPorProjeto.data"
            label="Horas"
          />
        </UCard>

        <UCard>
          <template #header>
            <div class="flex items-center gap-2">
              <UIcon
                name="i-lucide-trending-up"
                class="size-5 text-primary"
              />
              <h3 class="font-semibold">
                Valor Alocado por Projeto
              </h3>
            </div>
          </template>
          <template v-if="loading">
            <div class="flex h-72 flex-col justify-center gap-3 px-4">
              <USkeleton class="h-3 w-full" />
              <USkeleton class="h-3 w-4/5" />
              <USkeleton class="h-3 w-3/5" />
              <USkeleton class="h-3 w-4/5" />
              <USkeleton class="h-3 w-2/5" />
            </div>
          </template>
          <HomeLineChart
            v-else
            :labels="comprasPorProjeto.labels"
            :data="comprasPorProjeto.data"
            label="Valor (R$)"
          />
        </UCard>
      </div>
    </template>
  </UDashboardPanel>
</template>
