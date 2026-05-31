<script setup lang="ts">
import { computed, ref } from 'vue'

import type {
  ProgramaInvestimento,
  DimProjeto,
  FatoExecucao,
  FatoCompra,
  MateriaisPorProjeto
} from '~/types/api'

definePageMeta({
  layout: 'dashboard'
})

const pesquisa = ref('')

const {
  data: programas,
  status
} = useApi<ProgramaInvestimento[]>(
  '/api/programa/investimento'
)

const {
  data: projetos,
  status: projetosStatus
} = useApi<DimProjeto[]>(
  '/api/dim/projetos'
)

const {
  data: execucoes
} = useApi<FatoExecucao[]>(
  '/api/fato/execucao-tarefas'
)

const {
  data: compras
} = useApi<FatoCompra[]>(
  '/api/fato/compras'
)

const {
  data: materiais
} = useApi<MateriaisPorProjeto[]>(
  '/api/projetos/materiais'
)

const loading = computed(() =>
  status.value !== 'success'
  || projetosStatus.value !== 'success'
)

const projetosFiltrados = computed(() => {
  if (!projetos.value) {
    return []
  }

  return projetos.value.filter(projeto =>
    projeto.nome_projeto
      .toLowerCase()
      .includes(
        pesquisa.value.toLowerCase()
      )
  )
})

const projetosPorPrograma = computed(() => {
  const listaProjetos
    = pesquisa.value
      ? projetosFiltrados.value
      : projetos.value

  if (!listaProjetos) {
    return new Map<string, DimProjeto[]>()
  }

  const map = new Map<
    string,
    DimProjeto[]
  >()

  for (const p of listaProjetos) {
    const lista
      = map.get(p.codigo_programa)
        ?? []

    lista.push(p)

    map.set(
      p.codigo_programa,
      lista
    )
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
      <!-- Barra de Pesquisa -->
      <div class="mb-6">
        <div
          class="relative z-50 w-full max-w-sm"
        >
          <UInput
            v-model="pesquisa"
            type="text"
            placeholder="Pesquisar projeto..."
            icon="i-lucide-search"
            size="lg"
          />
        </div>
      </div>

      <!-- Loading -->
      <div
        v-if="loading"
        class="space-y-8"
      >
        <!-- Ranking Skeleton -->
        <div>
          <h2
            class="mb-4 text-lg font-semibold"
          >
            Ranking de Programas
          </h2>

          <div
            class="grid grid-cols-1 gap-4 sm:grid-cols-3"
          >
            <UCard
              v-for="i in 3"
              :key="i"
            >
              <div
                class="flex flex-col items-center gap-2 py-2"
              >
                <USkeleton
                  class="h-10 w-10 rounded-full"
                />

                <USkeleton
                  class="h-4 w-24"
                />

                <USkeleton
                  class="h-6 w-32"
                />
              </div>
            </UCard>
          </div>
        </div>

        <!-- Table Skeleton -->
        <UCard>
          <template #header>
            <div
              class="flex items-center justify-between"
            >
              <USkeleton
                class="h-5 w-48"
              />

              <div class="flex gap-3">
                <USkeleton
                  class="h-9 w-32"
                />

                <USkeleton
                  class="h-9 w-32"
                />
              </div>
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
        class="space-y-8"
      >
        <!-- Ranking -->
        <div>
          <h2
            class="mb-4 text-lg font-semibold"
          >
            Ranking de Programas
          </h2>

          <InvestmentRanking
            v-if="programas"
            :programas="programas"
            :projetos-por-programa="projetosPorPrograma"
          />
        </div>

        <!-- Resultado da pesquisa -->
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

                <h3 class="font-semibold">
                  Projetos Encontrados
                </h3>
              </div>
            </template>

            <div
              v-if="projetosFiltrados.length"
              class="space-y-2"
            >
              <div
                v-for="projeto in projetosFiltrados"
                :key="projeto.id_projeto"
                class="rounded-lg border border-gray-800 p-3"
              >
                <div class="font-medium">
                  {{ projeto.nome_projeto }}
                </div>

                <div
                  class="text-sm text-gray-400"
                >
                  Programa:
                  {{ projeto.nome_programa }}
                </div>
              </div>
            </div>

            <div
              v-else
              class="text-sm text-gray-400"
            >
              Nenhum projeto encontrado.
            </div>
          </UCard>
        </div>

        <!-- Tabela -->
        <InvestmentTable
          v-if="projetosFiltrados.length"
          :projetos="projetosFiltrados"
          :execucoes="execucoes ?? []"
          :compras="compras ?? []"
          :materiais="materiais ?? []"
        />
      </div>
    </template>
  </UDashboardPanel>
</template>
