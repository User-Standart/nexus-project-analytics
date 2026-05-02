<script setup lang="ts">
import type { MateriaisPorProjeto } from '~/types/api'

definePageMeta({
  layout: 'dashboard'
})

const { data: materiais, status } = useApi<MateriaisPorProjeto[]>('/api/projetos/materiais')

const loading = computed(() => status.value !== 'success')

const totalProjetos = computed(() => new Set(materiais.value?.map(m => m.codigo_projeto)).size)

const mediaPorMaterial = computed(() => {
  if (!materiais.value?.length) return 0
  const total = materiais.value.reduce((acc, m) => acc + m.quantidade_estoque, 0)
  return Math.round(total / materiais.value.length)
})

const materialMaisFrequente = computed(() => {
  if (!materiais.value?.length) return '-'
  const map = new Map<string, number>()
  for (const m of materiais.value) {
    map.set(m.descricao_material, (map.get(m.descricao_material) ?? 0) + 1)
  }
  return [...map.entries()].sort((a, b) => b[1] - a[1])[0]?.[0] ?? '-'
})

const stats = computed(() => [
  {
    label: 'Material mais frequente',
    value: materialMaisFrequente.value,
    icon: 'i-lucide-package-search'
  },
  {
    label: 'Projetos com materiais',
    value: totalProjetos.value,
    icon: 'i-lucide-folder-kanban'
  },
  {
    label: 'Média de estoque por material',
    value: mediaPorMaterial.value,
    icon: 'i-lucide-boxes'
  }
])
</script>

<template>
  <UDashboardPanel>
    <template #header>
      <UDashboardNavbar
        title="Materiais por Projeto"
        icon="i-lucide-package"
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
                  Distribuição de estoque — top 10
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
            <MaterialsBarChart
              v-if="!loading && materiais && materiais.length > 0"
              :materiais="materiais"
            />
          </UCard>

          <UCard v-if="loading">
            <template #header>
              <div class="flex items-center justify-between">
                <USkeleton class="h-5 w-48" />
                <USkeleton class="h-9 w-44" />
              </div>
            </template>
            <div class="space-y-3">
              <USkeleton
                v-for="i in 5"
                :key="i"
                class="h-10 w-full"
              />
            </div>
          </UCard>
          <MaterialsTable
            v-else-if="materiais"
            :materiais="materiais"
          />
        </div>
      </div>
    </template>
  </UDashboardPanel>
</template>
