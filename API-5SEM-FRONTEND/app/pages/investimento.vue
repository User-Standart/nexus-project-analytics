<script setup lang="ts">
import type { ProgramaInvestimento, DimProjeto } from '~/types/api'

definePageMeta({
  layout: 'dashboard'
})

const { data: programas, status } = await useApi<ProgramaInvestimento[]>('/api/programa/investimento')
const { data: projetos, status: projetosStatus } = await useApi<DimProjeto[]>('/api/dim/projetos')

const loading = computed(() => status.value === 'pending' || projetosStatus.value === 'pending')

const projetosPorPrograma = computed(() => {
  if (!projetos.value) return new Map<string, DimProjeto[]>()
  const map = new Map<string, DimProjeto[]>()
  for (const p of projetos.value) {
    const lista = map.get(p.codigo_programa) ?? []
    lista.push(p)
    map.set(p.codigo_programa, lista)
  }
  return map
})
</script>

<template>
  <UDashboardPanel>
    <template #header>
      <UDashboardNavbar
        title="Investimentos por Programa"
        icon="i-lucide-trending-up"
      >
        <template #right>
          <UColorModeButton />
        </template>
      </UDashboardNavbar>
    </template>

    <template #body>
      <div class="space-y-8">
        <div>
          <h2 class="mb-4 text-lg font-semibold">
            Ranking de Programas
          </h2>
          <template v-if="loading">
            <div class="grid grid-cols-1 gap-4 sm:grid-cols-3">
              <UCard
                v-for="i in 3"
                :key="i"
              >
                <div class="flex flex-col items-center gap-2 py-2">
                  <USkeleton class="h-10 w-10 rounded-full" />
                  <USkeleton class="h-4 w-24" />
                  <USkeleton class="h-6 w-32" />
                </div>
              </UCard>
            </div>
          </template>
          <InvestmentRanking
            v-else-if="programas"
            :programas="programas"
            :projetos-por-programa="projetosPorPrograma"
          />
        </div>

        <InvestmentTable
          v-if="projetos"
          :projetos="projetos"
        />
      </div>
    </template>
  </UDashboardPanel>
</template>
