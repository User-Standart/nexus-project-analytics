<script setup lang="ts">
import type { TableRow } from '@nuxt/ui'
import type { DimProjeto, FatoExecucao, FatoCompra, MateriaisPorProjeto } from '~/types/api'

const props = defineProps<{
  projetos: DimProjeto[]
  execucoes?: FatoExecucao[]
  compras?: FatoCompra[]
  materiais?: MateriaisPorProjeto[]
}>()

const programaFiltro = ref('Todos')
const statusFiltro = ref('Todos')
const pagina = ref(1)
const porPagina = 5
const selecionado = ref<DimProjeto | null>(null)

function handleSelect(_e: Event, row: TableRow<DimProjeto>) {
  selecionado.value = row.original
}

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

function formatBRL(value: number) {
  return value.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })
}

function initials(name: string | undefined) {
  if (!name) return '?'
  return name
    .split(' ')
    .filter(Boolean)
    .slice(0, 2)
    .map(n => n[0]?.toUpperCase() ?? '')
    .join('')
}

const columns = [
  { accessorKey: 'nome_projeto', header: 'Projeto' },
  { accessorKey: 'nome_programa', header: 'Programa' },
  { accessorKey: 'responsavel', header: 'Responsável' },
  { accessorKey: 'status', header: 'Status' },
  { accessorKey: 'data_inicio', header: 'Início' },
  { accessorKey: 'data_fim_prevista', header: 'Fim previsto' }
]

const detalhe = computed(() => {
  if (!selecionado.value) return null
  const projeto = selecionado.value
  const sk = projeto.sk_projeto

  const execucoesProjeto = (props.execucoes ?? []).filter(e => e.sk_projeto === sk)
  const comprasProjeto = (props.compras ?? []).filter(c => c.sk_projeto === sk)
  const materiaisProjeto = (props.materiais ?? []).filter(m => m.codigo_projeto === projeto.codigo_projeto)

  const totalHoras = execucoesProjeto.reduce((acc, e) => acc + Number(e.horas_trabalhadas), 0)
  const totalCompras = comprasProjeto.reduce((acc, c) => acc + Number(c.valor_total_pedido), 0)
  const valorAlocado = comprasProjeto.reduce((acc, c) => acc + Number(c.valor_alocado_projeto), 0)

  const inicio = new Date(projeto.data_inicio).getTime()
  const fim = new Date(projeto.data_fim_prevista).getTime()
  const hoje = Date.now()
  const duracaoTotal = fim - inicio
  const decorrido = Math.max(0, hoje - inicio)
  const progresso = duracaoTotal > 0 ? Math.min(100, Math.round((decorrido / duracaoTotal) * 100)) : 0

  return {
    projeto,
    totalHoras,
    totalCompras,
    valorAlocado,
    materiaisProjeto,
    comprasProjeto,
    progresso
  }
})

const materiaisColumns = [
  { accessorKey: 'codigo_material', header: 'Código' },
  { accessorKey: 'descricao_material', header: 'Material' },
  { accessorKey: 'quantidade_estoque', header: 'Estoque' }
]
</script>

<template>
  <UCard>
    <template #header>
      <div class="flex md:items-center justify-between md:flex-row flex-col gap-4">
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
      class="cursor-pointer"
      :ui="{ tr: 'hover:bg-elevated/50' }"
      @select="handleSelect"
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
            <UAvatar
              :alt="detalhe.projeto.responsavel"
              :text="initials(detalhe.projeto.responsavel)"
              size="lg"
              class="bg-primary/10 text-primary"
            />
            <div class="min-w-0 flex-1 space-y-1">
              <p class="text-xs uppercase tracking-wide text-muted">
                Projetos / {{ detalhe.projeto.codigo_projeto }}
              </p>
              <div class="flex flex-wrap items-center gap-2">
                <h2 class="text-xl font-semibold">
                  {{ detalhe.projeto.nome_projeto }}
                </h2>
                <UBadge
                  :color="statusColor(detalhe.projeto.status)"
                  variant="subtle"
                >
                  {{ detalhe.projeto.status }}
                </UBadge>
              </div>
              <p class="text-sm text-muted">
                {{ detalhe.projeto.nome_programa }}
                · resp. <span class="font-medium text-default">{{ detalhe.projeto.responsavel }}</span>
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
              label="Horas acumuladas"
              :value="`${detalhe.totalHoras.toFixed(1)}h`"
              icon="i-lucide-clock"
            />
            <AppStatCard
              label="Valor alocado"
              :value="formatBRL(detalhe.valorAlocado)"
              icon="i-lucide-banknote"
            />
            <AppStatCard
              label="Compras"
              :value="formatBRL(detalhe.totalCompras)"
              icon="i-lucide-shopping-cart"
              :hint="`${detalhe.comprasProjeto.length} pedido${detalhe.comprasProjeto.length === 1 ? '' : 's'}`"
            />
            <AppStatCard
              label="Progresso"
              :value="`${detalhe.progresso}%`"
              icon="i-lucide-trending-up"
            >
              <UProgress
                :model-value="detalhe.progresso"
                size="xs"
                class="mt-3"
              />
            </AppStatCard>
          </div>

          <UCard
            :ui="{ body: 'sm:p-4 p-4' }"
            variant="subtle"
          >
            <h3 class="mb-3 flex items-center gap-2 text-lg font-semibold">
              <UIcon
                name="i-lucide-info"
                class="size-6 text-primary"
              />
              Detalhes
            </h3>
            <dl class="grid grid-cols-1 gap-x-4 gap-y-3 sm:grid-cols-2">
              <div class="flex justify-between gap-4 border-b border-default pb-2 sm:border-0 sm:pb-0">
                <dt class="text-sm text-muted">
                  Código
                </dt>
                <dd class="font-medium">
                  {{ detalhe.projeto.codigo_projeto }}
                </dd>
              </div>
              <div class="flex justify-between gap-4 border-b border-default pb-2 sm:border-0 sm:pb-0">
                <dt class="text-sm text-muted">
                  Gerente
                </dt>
                <dd class="truncate font-medium">
                  {{ detalhe.projeto.gerente_programa }}
                </dd>
              </div>
              <div class="flex justify-between gap-4 border-b border-default pb-2 sm:border-0 sm:pb-0">
                <dt class="text-sm text-muted">
                  Início
                </dt>
                <dd class="font-medium">
                  {{ formatDate(detalhe.projeto.data_inicio) }}
                </dd>
              </div>
              <div class="flex justify-between gap-4">
                <dt class="text-sm text-muted">
                  Fim previsto
                </dt>
                <dd class="font-medium">
                  {{ formatDate(detalhe.projeto.data_fim_prevista) }}
                </dd>
              </div>
            </dl>
          </UCard>

          <div v-if="detalhe.materiaisProjeto.length">
            <h3 class="mb-3 flex items-center gap-2 text-sm font-semibold">
              <UIcon
                name="i-lucide-package"
                class="size-4 text-primary"
              />
              Materiais usados
              <UBadge
                color="neutral"
                variant="subtle"
                size="sm"
              >
                {{ detalhe.materiaisProjeto.length }}
              </UBadge>
            </h3>
            <UCard :ui="{ body: 'p-0' }">
              <UTable
                :data="detalhe.materiaisProjeto"
                :columns="materiaisColumns"
              />
            </UCard>
          </div>

          <div v-if="detalhe.comprasProjeto.length">
            <h3 class="mb-3 flex items-center gap-2 text-sm font-semibold">
              <UIcon
                name="i-lucide-shopping-cart"
                class="size-4 text-primary"
              />
              Solicitações de compra
              <UBadge
                color="neutral"
                variant="subtle"
                size="sm"
              >
                {{ detalhe.comprasProjeto.length }}
              </UBadge>
            </h3>
            <UCard :ui="{ body: 'p-0' }">
              <ul class="divide-y divide-default">
                <li
                  v-for="(c, i) in detalhe.comprasProjeto"
                  :key="c.sk_fato"
                  class="flex items-center justify-between gap-4 p-3 text-sm"
                >
                  <div class="flex items-center gap-3">
                    <UIcon
                      name="i-lucide-receipt"
                      class="size-4 text-muted"
                    />
                    <span class="text-muted">
                      Pedido {{ i + 1 }}
                    </span>
                  </div>
                  <div class="flex flex-col items-end">
                    <span class="font-medium">
                      {{ formatBRL(Number(c.valor_total_pedido)) }}
                    </span>
                    <span class="text-xs text-muted">
                      Alocado {{ formatBRL(Number(c.valor_alocado_projeto)) }}
                    </span>
                  </div>
                </li>
              </ul>
            </UCard>
          </div>
        </div>
      </template>
    </USlideover>
  </UCard>
</template>
