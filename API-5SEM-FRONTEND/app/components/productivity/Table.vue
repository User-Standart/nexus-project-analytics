<script setup lang="ts">
import type { FatoExecucao } from '~/types/api'

const props = defineProps<{
  execucoes: FatoExecucao[]
}>()

const responsavelFiltro = ref('Todos')
const pagina = ref(1)
const porPagina = 5

const responsaveis = computed(() => ['Todos', ...new Set(props.execucoes.map(e => e.sk_responsavel))])

const execucoesFiltradas = computed(() => {
  return props.execucoes.filter(e => responsavelFiltro.value === 'Todos' || e.sk_responsavel === responsavelFiltro.value)
})

const execucoesPaginadas = computed(() => {
  const inicio = (pagina.value - 1) * porPagina
  return execucoesFiltradas.value.slice(inicio, inicio + porPagina)
})

const totalPaginas = computed(() => Math.ceil(execucoesFiltradas.value.length / porPagina))

watch(responsavelFiltro, () => {
  pagina.value = 1
})

function formatDate(date: string) {
  return new Date(date).toLocaleDateString('pt-BR')
}

const columns = [
  { accessorKey: 'sk_responsavel', header: 'Responsável' },
  { accessorKey: 'sk_projeto', header: 'Projeto' },
  { accessorKey: 'sk_tempo', header: 'Data' },
  { accessorKey: 'horas_trabalhadas', header: 'Horas' }
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
            Execuções
          </h3>
        </div>
        <USelect
          v-model="responsavelFiltro"
          :items="responsaveis"
          placeholder="Responsável"
          class="w-48"
        />
      </div>
    </template>

    <UTable
      :data="execucoesPaginadas"
      :columns="columns"
    >
      <template #sk_tempo-cell="{ row }">
        {{ formatDate(row.original.sk_tempo) }}
      </template>
      <template #horas_trabalhadas-cell="{ row }">
        <UBadge
          color="neutral"
          variant="subtle"
        >
          {{ Number(row.original.horas_trabalhadas).toFixed(1) }}h
        </UBadge>
      </template>
    </UTable>

    <div class="mt-4 flex items-center justify-between text-sm text-gray-500">
      <span>{{ execucoesFiltradas.length }} execuções</span>
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
