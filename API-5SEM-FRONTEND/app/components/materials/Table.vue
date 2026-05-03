<script setup lang="ts">
import type { TableRow } from '@nuxt/ui'
import type { MateriaisPorProjeto } from '~/types/api'

const props = defineProps<{
  materiais: MateriaisPorProjeto[]
}>()

const projetoFiltro = ref('Todos')
const pagina = ref(1)
const porPagina = 5
const selecionado = ref<MateriaisPorProjeto | null>(null)

function handleSelect(_e: Event, row: TableRow<MateriaisPorProjeto>) {
  selecionado.value = row.original
}

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

const detalhe = computed(() => {
  if (!selecionado.value) return null
  const m = selecionado.value
  const ocorrencias = props.materiais.filter(x => x.codigo_material === m.codigo_material)
  const totalEstoque = ocorrencias.reduce((acc, x) => acc + x.quantidade_estoque, 0)
  const projetosDistintos = new Set(ocorrencias.map(x => x.codigo_projeto))
  return {
    material: m,
    ocorrencias,
    totalEstoque,
    quantidadeProjetos: projetosDistintos.size
  }
})

const ocorrenciasColumns = [
  { accessorKey: 'nome_projeto', header: 'Projeto' },
  { accessorKey: 'codigo_projeto', header: 'Código' },
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
      class="cursor-pointer"
      :ui="{ tr: 'hover:bg-elevated/50' }"
      @select="handleSelect"
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

    <USlideover
      :open="!!selecionado"
      :ui="{ content: 'sm:max-w-2xl' }"
      @update:open="(open) => !open && (selecionado = null)"
    >
      <template #header>
        <div
          v-if="detalhe"
          class="flex items-start gap-4 justify-between w-full"
        >
          <div class="flex items-start gap-4">
            <div class="flex size-12 shrink-0 items-center justify-center rounded-lg bg-primary/10">
              <UIcon
                name="i-lucide-package"
                class="size-6 text-primary"
              />
            </div>
            <div class="min-w-0 flex-1 space-y-1">
              <p class="text-xs uppercase tracking-wide text-muted">
                Materiais / {{ detalhe.material.codigo_material }}
              </p>
              <h2 class="text-xl font-semibold">
                {{ detalhe.material.descricao_material }}
              </h2>
              <p class="flex items-center gap-2 text-sm text-muted">
                Estoque em <span class="truncate font-medium text-default">{{ detalhe.material.nome_projeto }}</span>
                <UBadge
                  :color="estoqueColor(detalhe.material.quantidade_estoque)"
                  variant="subtle"
                >
                  {{ detalhe.material.quantidade_estoque }}
                </UBadge>
              </p>
            </div>
          </div>
          <UButton
            color="neutral"
            variant="ghost"
            icon="i-lucide-x"
            aria-label="Fechar"
            @click="selecionado = null"
          />
        </div>
      </template>

      <template #body>
        <div
          v-if="detalhe"
          class="space-y-6"
        >
          <div class="grid grid-cols-1 gap-3 sm:grid-cols-2">
            <AppStatCard
              label="Estoque total"
              :value="detalhe.totalEstoque"
              icon="i-lucide-boxes"
              hint="todos os projetos"
            />
            <AppStatCard
              label="Projetos que usam"
              :value="detalhe.quantidadeProjetos"
              icon="i-lucide-folder-kanban"
            />
          </div>

          <div>
            <h3 class="mb-3 flex items-center gap-2 text-sm font-semibold">
              <UIcon
                name="i-lucide-folder-kanban"
                class="size-4 text-primary"
              />
              Onde este material aparece
              <UBadge
                color="neutral"
                variant="subtle"
                size="sm"
              >
                {{ detalhe.ocorrencias.length }}
              </UBadge>
            </h3>
            <UCard :ui="{ body: 'sm:p-0 p-0' }">
              <UTable
                :data="detalhe.ocorrencias"
                :columns="ocorrenciasColumns"
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
            </UCard>
          </div>
        </div>
      </template>
    </USlideover>
  </UCard>
</template>
