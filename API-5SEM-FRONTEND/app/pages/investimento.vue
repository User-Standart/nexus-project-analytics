<script setup lang="ts">
import type { ProgramaInvestimento } from '~/types/api'

definePageMeta({
  layout: 'dashboard'
})

const { data: programas, status } = await useFetch<ProgramaInvestimento[]>('/proxy/api/programa/investimento')

const loading = computed(() => status.value === 'pending')
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
          />
        </div>

        <UCard>
          <template #header>
            <div class="flex items-center gap-2">
              <UIcon
                name="i-lucide-bar-chart-3"
                class="size-5 text-primary"
              />
              <h3 class="font-semibold">
                Investimento por Programa
              </h3>
            </div>
          </template>
          <template v-if="loading">
            <div class="flex h-72 items-end gap-3 px-4">
              <USkeleton
                v-for="i in 3"
                :key="i"
                class="flex-1 rounded-t"
                :style="{ height: `${40 + i * 20}%` }"
              />
            </div>
          </template>
          <InvestmentBarChart
            v-else-if="programas"
            :programas="programas"
          />
        </UCard>
      </div>
    </template>
  </UDashboardPanel>
</template>
