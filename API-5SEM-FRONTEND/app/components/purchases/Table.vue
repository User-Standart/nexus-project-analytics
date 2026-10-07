<script setup lang="ts">
import type { TableRow } from '@nuxt/ui'
import type { Purchase } from '~/types/api'
import {
  filterPurchases,
  purchaseStatusOptions,
  formatDuration,
  statusColor,
  tipoColor
} from '~/utils/purchases'

function formatDate(date: string) {
  return new Date(date).toLocaleDateString('pt-BR')
}

const props = defineProps<{
  pedidos: Purchase[]
}>()

const tipoFiltro = ref('Todos')
const statusFiltro = ref('Todos')
const pagina = ref(1)
const porPagina = 8
const selecionado = ref<Purchase | null>(null)

function handleSelect(_e: Event, row: TableRow<Purchase>) {
  selecionado.value = row.original
}

const tipos = ['Todos', 'SC', 'PC']
const statuses = computed(() => purchaseStatusOptions(props.pedidos))

const pedidosFiltrados = computed(() =>
  filterPurchases(props.pedidos, {
    tipo: tipoFiltro.value,
    status: statusFiltro.value
  })
)

const pedidosPaginados = computed(() => {
  const inicio = (pagina.value - 1) * porPagina
  return pedidosFiltrados.value.slice(inicio, inicio + porPagina)
})

const totalPaginas = computed(() =>
  Math.max(1, Math.ceil(pedidosFiltrados.value.length / porPagina))
)

watch([tipoFiltro, statusFiltro], () => {
  pagina.value = 1
})

const columns = [
  { accessorKey: 'type', header: 'Tipo' },
  { accessorKey: 'numero', header: 'Número' },
  { accessorKey: 'status', header: 'Status' },
  { accessorKey: 'data_criacao', header: 'Criação' },
  { accessorKey: 'data_previsao_entrega', header: 'Previsão entrega' },
  { accessorKey: 'duracao_dias', header: 'Duração' },
  { accessorKey: 'atrasado', header: 'Situação' }
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
            Solicitações e pedidos de compra
          </h3>
        </div>
        <div class="flex gap-3">
          <USelect
            v-model="tipoFiltro"
            :items="tipos"
            placeholder="Tipo"
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
      :data="pedidosPaginados"
      :columns="columns"
      class="cursor-pointer"
      :ui="{ tr: 'hover:bg-elevated/50' }"
      @select="handleSelect"
    >
      <template #type-cell="{ row }">
        <UBadge
          :color="tipoColor(row.original.type)"
          variant="subtle"
        >
          {{ row.original.type }}
        </UBadge>
      </template>
      <template #status-cell="{ row }">
        <UBadge
          :color="statusColor(row.original.status)"
          variant="subtle"
        >
          {{ row.original.status }}
        </UBadge>
      </template>
      <template #data_criacao-cell="{ row }">
        {{ formatDate(row.original.data_criacao) }}
      </template>
      <template #data_previsao_entrega-cell="{ row }">
        {{ row.original.data_previsao_entrega ? formatDate(row.original.data_previsao_entrega) : '-' }}
      </template>
      <template #duracao_dias-cell="{ row }">
        <span :class="row.original.atrasado ? 'font-semibold text-error' : ''">
          {{ formatDuration(row.original.duracao_dias) }}
        </span>
      </template>
      <template #atrasado-cell="{ row }">
        <UBadge
          v-if="row.original.atrasado"
          color="error"
          variant="subtle"
          icon="i-lucide-triangle-alert"
        >
          Atrasado
        </UBadge>
        <span
          v-else-if="row.original.type === 'PC'"
          class="text-sm text-muted"
        >
          No prazo
        </span>
        <span
          v-else
          class="text-sm text-muted"
        >
          —
        </span>
      </template>
    </UTable>

    <div class="mt-4 flex items-center justify-between text-sm text-gray-500">
      <span>{{ pedidosFiltrados.length }} pedidos</span>
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
      :ui="{ content: 'sm:max-w-xl' }"
      @update:open="(open) => !open && (selecionado = null)"
    >
      <template #header>
        <div
          v-if="selecionado"
          class="flex items-start gap-4 justify-between w-full"
        >
          <div class="min-w-0 flex-1 space-y-1">
            <p class="text-xs uppercase tracking-wide text-muted">
              {{ selecionado.type === 'PC' ? 'Pedido de compra' : 'Solicitação de compra' }}
            </p>
            <div class="flex flex-wrap items-center gap-2">
              <h2 class="text-xl font-semibold">
                {{ selecionado.numero }}
              </h2>
              <UBadge
                :color="statusColor(selecionado.status)"
                variant="subtle"
              >
                {{ selecionado.status }}
              </UBadge>
              <UBadge
                v-if="selecionado.atrasado"
                color="error"
                variant="subtle"
                icon="i-lucide-triangle-alert"
              >
                Atrasado
              </UBadge>
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
          v-if="selecionado"
          class="space-y-6"
        >
          <div class="grid grid-cols-1 gap-3 sm:grid-cols-2">
            <AppStatCard
              label="Tipo"
              :value="selecionado.type === 'PC' ? 'Pedido (PC)' : 'Solicitação (SC)'"
              icon="i-lucide-tag"
            />
            <AppStatCard
              label="Duração"
              :value="formatDuration(selecionado.duracao_dias)"
              icon="i-lucide-timer"
              :icon-class="selecionado.atrasado ? 'text-error' : ''"
            />
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
                  Número
                </dt>
                <dd class="font-medium">
                  {{ selecionado.numero }}
                </dd>
              </div>
              <div class="flex justify-between gap-4 border-b border-default pb-2 sm:border-0 sm:pb-0">
                <dt class="text-sm text-muted">
                  Status
                </dt>
                <dd class="font-medium">
                  {{ selecionado.status }}
                </dd>
              </div>
              <div class="flex justify-between gap-4 border-b border-default pb-2 sm:border-0 sm:pb-0">
                <dt class="text-sm text-muted">
                  Data de criação
                </dt>
                <dd class="font-medium">
                  {{ formatDate(selecionado.data_criacao) }}
                </dd>
              </div>
              <div class="flex justify-between gap-4">
                <dt class="text-sm text-muted">
                  Previsão de entrega
                </dt>
                <dd class="font-medium">
                  {{ selecionado.data_previsao_entrega ? formatDate(selecionado.data_previsao_entrega) : '-' }}
                </dd>
              </div>
            </dl>
          </UCard>
        </div>
      </template>
    </USlideover>
  </UCard>
</template>
