<script setup lang="ts">
import type { MateriaisPorProjeto } from '~/types/api'

const props = defineProps<{
  materiais: MateriaisPorProjeto[]
}>()

const projetoFiltro = ref('Todos')
const pagina = ref(1)
const porPagina = 5

const projetos = computed(() => ['Todos', ...new Set(props.materiais.map(m => m.nome_projeto))])

const materiaisFiltrados = computed(() => {
  return props.materiais.filter(m => projetoFiltro.value === 'Todos' || m.nome_projeto === projetoFiltro.value)
})

const materiaisPaginados = computed(() => {
  const inicio = (pagina.value - 1) * porPagina
  return materiaisFiltrados.value.slice(inicio, inicio + porPagina)
})

const totalPaginas = computed(() => Math.ceil(materiaisFiltrados.value.length / porPagina))

watch(projetoFiltro, () => {
  pagina.value = 1
})

function estoqueColor(qtd: number) {
  if (qtd === 0) return 'error'
  if (qtd < 10) return 'warning'
  return 'success'
}

const columns = [
  { accessorKey: 'nome_projeto', header: 'Projeto' },
  { accessorKey: 'codigo_material', header: 'Código' },
  { accessorKey: 'descricao_material', header: 'Material' },
  { accessorKey: 'quantidade_estoque', header: 'Estoque' }
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
            Materiais por projeto
          </h3>
        </div>
        <USelect
          v-model="projetoFiltro"
          :items="projetos"
          placeholder="Projeto"
          class="w-44"
        />
      </div>
    </template>

    <UTable
      :data="materiaisPaginados"
      :columns="columns"
    >
      <template #quantidade_estoque-cell="{ row }">
        <UBadge
          :color="estoqueColor(row.original.quantidade_estoque)"
          variant="subtle"
        >
          {{ row.original.quantidade_estoque }}
        </UBadge>
      </template>
    </UTable>

    <div class="mt-4 flex items-center justify-between text-sm text-gray-500">
      <span>{{ materiaisFiltrados.length }} materiais</span>
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
