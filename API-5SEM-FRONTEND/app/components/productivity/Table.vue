<script setup lang="ts">
import type { TableRow } from '@nuxt/ui'
import type { FatoExecucao, DimProjeto, DimTarefa } from '~/types/api'

const props = defineProps<{
  execucoes: FatoExecucao[]
  projetos?: DimProjeto[]
  tarefas?: DimTarefa[]
}>()

const responsavelFiltro = ref('Todos')
const pagina = ref(1)
const porPagina = 5
const selecionado = ref<FatoExecucao | null>(null)

function handleSelect(_e: Event, row: TableRow<FatoExecucao>) {
  selecionado.value = row.original
}

const responsaveis = computed(() => ['Todos', ...new Set(props.execucoes.map(e => e.sk_responsavel))])

const execucoesFiltradas = computed(() => {
  return props.execucoes.filter(e => responsavelFiltro.value === 'Todos' || e.sk_responsavel === responsavelFiltro.value)
})

const execucoesPaginadas = computed(() => {
  const inicio = (pagina.value - 1) * porPagina
  return execucoesFiltradas.value.slice(inicio, inicio + porPagina)
})

const totalPaginas = computed(() => Math.ceil(execucoesFiltradas.value.length / porPagina))

watch(responsavelFiltro, () => {
  pagina.value = 1
})

function formatDate(date: string) {
  return new Date(date).toLocaleDateString('pt-BR')
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
  { accessorKey: 'sk_responsavel', header: 'Responsável' },
  { accessorKey: 'sk_projeto', header: 'Projeto' },
  { accessorKey: 'sk_tempo', header: 'Data' },
  { accessorKey: 'horas_trabalhadas', header: 'Horas' }
]

const projetoMap = computed(() =>
  new Map((props.projetos ?? []).map(p => [p.sk_projeto, p]))
)

const tarefaMap = computed(() =>
  new Map((props.tarefas ?? []).map(t => [t.sk_tarefa, t]))
)

const detalhe = computed(() => {
  if (!selecionado.value) return null
  const e = selecionado.value
  const projeto = projetoMap.value.get(e.sk_projeto)
  const tarefa = tarefaMap.value.get(e.sk_tarefa)

  const totalResponsavel = props.execucoes
    .filter(x => x.sk_responsavel === e.sk_responsavel)
    .reduce((acc, x) => acc + Number(x.horas_trabalhadas), 0)

  const execucoesResponsavel = props.execucoes.filter(x => x.sk_responsavel === e.sk_responsavel).length

  const totalProjeto = props.execucoes
    .filter(x => x.sk_projeto === e.sk_projeto)
    .reduce((acc, x) => acc + Number(x.horas_trabalhadas), 0)

  return {
    execucao: e,
    projeto,
    tarefa,
    totalResponsavel,
    execucoesResponsavel,
    totalProjeto
  }
})
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
            Execuções
          </h3>
        </div>
        <USelect
          v-model="responsavelFiltro"
          :items="responsaveis"
          placeholder="Responsável"
          class="w-48"
        />
      </div>
    </template>

    <UTable
      :data="execucoesPaginadas"
      :columns="columns"
      class="cursor-pointer"
      :ui="{ tr: 'hover:bg-elevated/50' }"
      @select="handleSelect"
    >
      <template #sk_tempo-cell="{ row }">
        {{ formatDate(row.original.sk_tempo) }}
      </template>
      <template #horas_trabalhadas-cell="{ row }">
        <UBadge
          color="neutral"
          variant="subtle"
        >
          {{ Number(row.original.horas_trabalhadas).toFixed(1) }}h
        </UBadge>
      </template>
    </UTable>

    <div class="mt-4 flex items-center justify-between text-sm text-gray-500">
      <span>{{ execucoesFiltradas.length }} execuções</span>
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
              :alt="detalhe.execucao.sk_responsavel"
              :text="initials(detalhe.execucao.sk_responsavel)"
              size="lg"
              class="bg-primary/10 text-primary"
            />
            <div class="min-w-0 flex-1 space-y-1">
              <p class="text-xs uppercase tracking-wide text-muted">
                Execuções / {{ detalhe.execucao.sk_fato }}
              </p>
              <h2 class="text-xl font-semibold">
                {{ detalhe.tarefa?.titulo ?? `Tarefa ${detalhe.execucao.sk_tarefa}` }}
              </h2>
              <p class="text-sm text-muted">
                {{ detalhe.projeto?.nome_projeto ?? `Projeto ${detalhe.execucao.sk_projeto}` }}
                · {{ formatDate(detalhe.execucao.sk_tempo) }}
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
              label="Horas nesta execução"
              :value="`${Number(detalhe.execucao.horas_trabalhadas).toFixed(1)}h`"
              icon="i-lucide-clock"
            />
            <AppStatCard
              label="Total do responsável"
              :value="`${detalhe.totalResponsavel.toFixed(1)}h`"
              icon="i-lucide-user-check"
              :hint="`em ${detalhe.execucoesResponsavel} execuç${detalhe.execucoesResponsavel === 1 ? 'ão' : 'ões'}`"
            />
            <AppStatCard
              label="Total do projeto"
              :value="`${detalhe.totalProjeto.toFixed(1)}h`"
              icon="i-lucide-folder-kanban"
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
            <dl class="grid grid-cols-1 gap-x-6 gap-y-3 sm:grid-cols-2">
              <div class="flex justify-between gap-4 border-b border-default pb-2 sm:border-0 sm:pb-0">
                <dt class="text-sm text-muted">
                  Responsável
                </dt>
                <dd class="truncate font-medium">
                  {{ detalhe.execucao.sk_responsavel }}
                </dd>
              </div>
              <div class="flex justify-between gap-4 border-b border-default pb-2 sm:border-0 sm:pb-0">
                <dt class="text-sm text-muted">
                  Projeto
                </dt>
                <dd class="truncate font-medium">
                  {{ detalhe.projeto?.nome_projeto ?? '—' }}
                </dd>
              </div>
              <div
                v-if="detalhe.projeto"
                class="flex justify-between gap-4 border-b border-default pb-2 sm:border-0 sm:pb-0"
              >
                <dt class="text-sm text-muted">
                  Programa
                </dt>
                <dd class="truncate font-medium">
                  {{ detalhe.projeto.nome_programa }}
                </dd>
              </div>
              <div
                v-if="detalhe.tarefa"
                class="flex items-center justify-between gap-4 border-b border-default pb-2 sm:border-0 sm:pb-0"
              >
                <dt class="text-sm text-muted">
                  Status da tarefa
                </dt>
                <dd>
                  <UBadge
                    color="neutral"
                    variant="subtle"
                  >
                    {{ detalhe.tarefa.status }}
                  </UBadge>
                </dd>
              </div>
              <div
                v-if="detalhe.tarefa"
                class="flex justify-between gap-4 border-b border-default pb-2 sm:border-0 sm:pb-0"
              >
                <dt class="text-sm text-muted">
                  Estimativa da tarefa
                </dt>
                <dd class="font-medium">
                  {{ Number(detalhe.tarefa.estimativa_horas).toFixed(1) }}h
                </dd>
              </div>
              <div class="flex justify-between gap-4">
                <dt class="text-sm text-muted">
                  Data
                </dt>
                <dd class="font-medium">
                  {{ formatDate(detalhe.execucao.sk_tempo) }}
                </dd>
              </div>
            </dl>
          </UCard>
        </div>
      </template>
    </USlideover>
  </UCard>
</template>
