<script setup lang="ts">
import type { DimProjeto } from '~/types/api'

const props = defineProps<{
  projetos: DimProjeto[]
}>()

const programaFiltro = ref('Todos')
const statusFiltro = ref('Todos')
const pagina = ref(1)
const porPagina = 5

const programas = computed(() => ['Todos', ...new Set(props.projetos.map(p => p.nome_programa))])
const statuses = computed(() => ['Todos', ...new Set(props.projetos.map(p => p.status))])

const projetosFiltrados = computed(() => {
  return props.projetos.filter((p) => {
    const matchPrograma = programaFiltro.value === 'Todos' || p.nome_programa === programaFiltro.value
    const matchStatus = statusFiltro.value === 'Todos' || p.status === statusFiltro.value
    return matchPrograma && matchStatus
  })
})

const projetosPaginados = computed(() => {
  const inicio = (pagina.value - 1) * porPagina
  return projetosFiltrados.value.slice(inicio, inicio + porPagina)
})

const totalPaginas = computed(() => Math.ceil(projetosFiltrados.value.length / porPagina))

watch([programaFiltro, statusFiltro], () => {
  pagina.value = 1
})

function statusColor(status: string) {
  if (status === 'Concluído') return 'success'
  if (status === 'Em andamento') return 'info'
  if (status === 'Planejamento') return 'warning'
  if (status === 'Suspenso') return 'error'
  return 'neutral'
}

function formatDate(date: string) {
  return new Date(date).toLocaleDateString('pt-BR')
}

const columns = [
  { accessorKey: 'nome_projeto', header: 'Projeto' },
  { accessorKey: 'nome_programa', header: 'Programa' },
  { accessorKey: 'responsavel', header: 'Responsável' },
  { accessorKey: 'status', header: 'Status' },
  { accessorKey: 'data_inicio', header: 'Início' },
  { accessorKey: 'data_fim_prevista', header: 'Fim previsto' }
]
</script>

<template>
  <UCard>
    <template #header>
      <div class="flex items-center justify-between">
        <div class="flex items-center gap-2">
          <UIcon
            name="i-lucide-table"
            class="size-5 text-primary"
          />
          <h3 class="font-semibold">
            Projetos por programa
          </h3>
        </div>
        <div class="flex gap-3">
          <USelect
            v-model="programaFiltro"
            :items="programas"
            placeholder="Programa"
          />
          <USelect
            v-model="statusFiltro"
            :items="statuses"
            placeholder="Status"
          />
        </div>
      </div>
    </template>

    <UTable
      :data="projetosPaginados"
      :columns="columns"
    >
      <template #status-cell="{ row }">
        <UBadge
          :color="statusColor(row.original.status)"
          variant="subtle"
        >
          {{ row.original.status }}
        </UBadge>
      </template>
      <template #data_inicio-cell="{ row }">
        {{ formatDate(row.original.data_inicio) }}
      </template>
      <template #data_fim_prevista-cell="{ row }">
        {{ formatDate(row.original.data_fim_prevista) }}
      </template>
    </UTable>

    <div class="mt-4 flex items-center justify-between text-sm text-gray-500">
      <span>{{ projetosFiltrados.length }} projetos</span>
      <div class="flex items-center gap-2">
        <UButton
          icon="i-lucide-chevron-left"
          variant="ghost"
          :disabled="pagina === 1"
          @click="pagina--"
        />
        <span>{{ pagina }} / {{ totalPaginas }}</span>
        <UButton
          icon="i-lucide-chevron-right"
          variant="ghost"
          :disabled="pagina === totalPaginas"
          @click="pagina++"
        />
      </div>
    </div>
  </UCard>
</template>
