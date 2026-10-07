<script setup lang="ts">
import { computed, ref } from 'vue'

import type {
  FatoExecucao,
  TempoGasto,
  DimProjeto,
  DimTarefa
} from '~/types/api'

definePageMeta({
  layout: 'dashboard'
})

const pesquisa = ref('')

const {
  data: execucoes,
  status
} = useApi<FatoExecucao[]>(
  '/api/fato/execucao-tarefas'
)

const {
  status: tempoGastoStatus
} = useApi<TempoGasto>(
  '/api/dim/tempo-gasto'
)

const {
  data: projetos
} = useApi<DimProjeto[]>(
  '/api/dim/projetos'
)

const {
  data: tarefas
} = useApi<DimTarefa[]>(
  '/api/dim/tarefas'
)

const loading = computed(() =>
  status.value !== 'success'
  || tempoGastoStatus.value !== 'success'
)

const execucoesFiltradas = computed(() => {
  if (!execucoes.value) {
    return []
  }

  return execucoes.value.filter(execucao =>
    execucao.sk_responsavel
      .toLowerCase()
      .includes(
        pesquisa.value.toLowerCase()
      )
  )
})

const mediaPorExecucao = computed(() => {
  if (!execucoesFiltradas.value.length) {
    return 0
  }

  const total
    = execucoesFiltradas.value.reduce(
      (acc, e) =>
        acc + Number(e.horas_trabalhadas),
      0
    )

  return (
    total / execucoesFiltradas.value.length
  ).toFixed(1)
})

const totalHoras = computed(() => {
  return execucoesFiltradas.value.reduce(
    (acc, e) =>
      acc + Number(e.horas_trabalhadas),
    0
  )
})

const stats = computed(() => [
  {
    label: 'Total de horas registradas',
    value: `${totalHoras.value.toFixed(1)}h`,
    icon: 'i-lucide-clock'
  },
  {
    label: 'Média de horas por execução',
    value: `${mediaPorExecucao.value}h`,
    icon: 'i-lucide-bar-chart-2'
  }
])
</script>

<template>
  <UDashboardPanel>
    <template #header>
      <UDashboardNavbar
        title="Horas Trabalhadas"
        icon="i-lucide-activity"
      >
        <template #right>
          <UColorModeButton />
        </template>
      </UDashboardNavbar>
    </template>

    <template #body>
      <div class="relative z-50">
        <!-- Barra de Pesquisa -->
        <div class="mb-6">
          <div
            class="w-full max-w-sm"
          >
            <UInput
              v-model="pesquisa"
              type="text"
              placeholder="Pesquisar responsável..."
              icon="i-lucide-search"
              size="lg"
            />
          </div>
        </div>

        <!-- Loading -->
        <div
          v-if="loading"
          class="space-y-6"
        >
          <!-- Cards Skeleton -->
          <div
            class="grid grid-cols-1 gap-4 sm:grid-cols-2"
          >
            <UCard
              v-for="i in 2"
              :key="i"
            >
              <div
                class="flex items-center justify-between"
              >
                <div class="space-y-2">
                  <USkeleton
                    class="h-4 w-24"
                  />

                  <USkeleton
                    class="h-8 w-20"
                  />
                </div>

                <USkeleton
                  class="size-8 rounded-full"
                />
              </div>
            </UCard>
          </div>

          <!-- Table Skeleton -->
          <UCard>
            <template #header>
              <div
                class="flex items-center justify-between"
              >
                <USkeleton
                  class="h-5 w-32"
                />

                <USkeleton
                  class="h-9 w-48"
                />
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
        </div>

        <!-- Conteúdo -->
        <div
          v-else
          class="space-y-6"
        >
          <!-- Cards -->
          <div
            class="grid grid-cols-1 gap-4 sm:grid-cols-2"
          >
            <UCard
              v-for="stat in stats"
              :key="stat.label"
            >
              <div
                class="flex items-center justify-between"
              >
                <div>
                  <p
                    class="text-sm text-gray-500"
                  >
                    {{ stat.label }}
                  </p>

                  <p
                    class="mt-1 truncate text-xl font-bold"
                  >
                    {{ stat.value }}
                  </p>
                </div>

                <UIcon
                  :name="stat.icon"
                  class="size-8 text-primary"
                />
              </div>
            </UCard>
          </div>

          <!-- Resultados -->
          <div v-if="pesquisa">
            <UCard>
              <template #header>
                <div
                  class="flex items-center gap-2"
                >
                  <UIcon
                    name="i-lucide-search"
                    class="size-5 text-primary"
                  />

                  <h3
                    class="font-semibold"
                  >
                    Responsáveis Encontrados
                  </h3>
                </div>
              </template>

              <div
                v-if="execucoesFiltradas.length"
                class="space-y-2"
              >
                <div
                  v-for="(execucao, index) in execucoesFiltradas.slice(0, 10)"
                  :key="index"
                  class="rounded-lg border border-gray-800 p-3"
                >
                  >
                  <div class="font-medium">
                    {{ execucao.sk_responsavel }}
                  </div>

                  <div
                    class="text-sm text-gray-400"
                  >
                    Horas:
                    {{ execucao.horas_trabalhadas }}
                  </div>

                  <div
                    class="text-sm text-gray-400"
                  >
                    Projeto:
                    {{ execucao.sk_projeto }}
                  </div>
                </div>
              </div>

              <div
                v-else
                class="text-sm text-gray-400"
              >
                Nenhum responsável encontrado.
              </div>
            </UCard>
          </div>

          <!-- Gráfico + tabela -->
          <div
            class="grid grid-cols-1 gap-6 lg:grid-cols-2"
          >
            <UCard>
              <template #header>
                <div
                  class="flex items-center gap-2"
                >
                  <UIcon
                    name="i-lucide-bar-chart-horizontal"
                    class="size-5 text-primary"
                  />

                  <h3
                    class="font-semibold"
                  >
                    Horas por responsável — top 10
                  </h3>
                </div>
              </template>

              <ProductivityBarChart
                v-if="execucoesFiltradas.length"
                :execucoes="execucoesFiltradas"
              />
            </UCard>

            <ProductivityTable
              v-if="execucoesFiltradas.length"
              :execucoes="execucoesFiltradas"
              :projetos="projetos ?? []"
              :tarefas="tarefas ?? []"
            />
          </div>
        </div>
      </div>
    </template>
  </UDashboardPanel>
</template>
