<script setup lang="ts">
import { computed } from 'vue'
import type { Purchase } from '~/types/api'
import { computeMetrics } from '~/utils/purchases'

definePageMeta({
  layout: 'dashboard'
})

const {
  data: pedidos,
  status
} = useApi<Purchase[]>('/api/purchases')

const loading = computed(() => status.value !== 'success')

const lista = computed(() => pedidos.value ?? [])

const metrics = computed(() => computeMetrics(lista.value))

const stats = computed(() => [
  {
    label: 'Solicitações (SC)',
    value: metrics.value.totalSC,
    icon: 'i-lucide-file-text'
  },
  {
    label: 'Pedidos (PC)',
    value: metrics.value.totalPC,
    icon: 'i-lucide-shopping-cart'
  },
  {
    label: 'Duração média PC',
    value: `${metrics.value.avgDurationPC.toFixed(1)} dias`,
    icon: 'i-lucide-timer'
  },
  {
    label: 'Pedidos atrasados',
    value: metrics.value.atrasados,
    icon: 'i-lucide-triangle-alert',
    iconClass: metrics.value.atrasados > 0 ? 'text-error' : ''
  }
])
</script>

<template>
  <UDashboardPanel>
    <template #header>
      <UDashboardNavbar
        title="Pedidos de Compra"
        icon="i-lucide-shopping-cart"
      >
        <template #right>
          <UColorModeButton />
        </template>
      </UDashboardNavbar>
    </template>

    <template #body>
      <!-- Loading -->
      <div
        v-if="loading"
        class="space-y-6"
      >
        <div class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
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
        </div>

        <div class="grid grid-cols-1 gap-6 lg:grid-cols-2">
          <UCard>
            <template #header>
              <USkeleton class="h-5 w-48" />
            </template>
            <USkeleton class="h-80 w-full" />
          </UCard>
          <UCard>
            <template #header>
              <USkeleton class="h-5 w-48" />
            </template>
            <div class="space-y-3">
              <USkeleton
                v-for="i in 6"
                :key="i"
                class="h-10 w-full"
              />
            </div>
          </UCard>
        </div>
      </div>

      <!-- Conteúdo -->
      <div
        v-else
        class="space-y-6"
      >
        <!-- Cards -->
        <div class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <AppStatCard
            v-for="stat in stats"
            :key="stat.label"
            :label="stat.label"
            :value="stat.value"
            :icon="stat.icon"
            :icon-class="stat.iconClass"
          />
        </div>

        <!-- Gráfico + tabela -->
        <div class="grid grid-cols-1 gap-6 lg:grid-cols-2">
          <UCard>
            <template #header>
              <div class="flex items-center gap-2">
                <UIcon
                  name="i-lucide-activity"
                  class="size-5 text-primary"
                />
                <h3 class="font-semibold">
                  Ciclo de vida — pedidos por status
                </h3>
              </div>
            </template>

            <PurchasesLifecycleChart
              v-if="lista.length"
              :pedidos="lista"
            />
            <p
              v-else
              class="py-12 text-center text-sm text-muted"
            >
              Sem dados para exibir.
            </p>
          </UCard>

          <PurchasesTable
            v-if="lista.length"
            :pedidos="lista"
          />
          <UCard v-else>
            <p class="py-12 text-center text-sm text-muted">
              Nenhum pedido de compra encontrado.
            </p>
          </UCard>
        </div>
      </div>
    </template>
  </UDashboardPanel>
</template>
