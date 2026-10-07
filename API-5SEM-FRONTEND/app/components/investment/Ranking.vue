<script setup lang="ts">
import type { ProgramaInvestimento, DimProjeto } from '~/types/api'

const props = defineProps<{
  programas: ProgramaInvestimento[]
  projetosPorPrograma: Map<string, DimProjeto[]>
}>()

const top3 = computed(() =>
  [...props.programas]
    .sort((a, b) => Number(b.investimento_total) - Number(a.investimento_total))
    .slice(0, 3)
)

function initials(name: string | undefined) {
  if (!name) return '?'
  return name
    .split(' ')
    .filter(Boolean)
    .slice(0, 2)
    .map(n => n[0]?.toUpperCase() ?? '')
    .join('')
}

function formatBRL(value: string | number) {
  return Number(value).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })
}

const ranks = [
  {
    label: '1º lugar',
    icon: 'i-lucide-trophy',
    iconClass: 'text-yellow-400',
    ringClass: 'ring-yellow-400/40',
    badgeColor: 'warning' as const
  },
  {
    label: '2º lugar',
    icon: 'i-lucide-medal',
    iconClass: 'text-slate-300',
    ringClass: 'ring-default',
    badgeColor: 'neutral' as const
  },
  {
    label: '3º lugar',
    icon: 'i-lucide-award',
    iconClass: 'text-amber-700',
    ringClass: 'ring-default',
    badgeColor: 'neutral' as const
  }
]
</script>

<template>
  <div class="grid grid-cols-1 gap-4 sm:grid-cols-3">
    <UCard
      v-for="(programa, index) in top3"
      :key="programa.codigo_programa"
      :class="['ring-1', ranks[index]?.ringClass, index === 0 && 'sm:scale-[1.02]']"
      :ui="{ body: 'p-5' }"
    >
      <div class="flex items-start justify-between">
        <UBadge
          :color="ranks[index]?.badgeColor"
          variant="subtle"
          size="sm"
        >
          {{ ranks[index]?.label }}
        </UBadge>
        <UIcon
          :name="ranks[index]?.icon ?? 'i-lucide-trophy'"
          :class="[ranks[index]?.iconClass, 'size-8']"
        />
      </div>

      <div class="mt-3 space-y-1">
        <p class="text-xs uppercase tracking-wide text-muted">
          Programa
        </p>
        <p class="truncate text-lg font-semibold">
          {{ programa.nome_programa }}
        </p>
      </div>

      <div class="mt-4">
        <p class="text-xs uppercase tracking-wide text-muted">
          Investimento total
        </p>
        <p class="text-2xl font-bold text-primary">
          {{ formatBRL(programa.investimento_total) }}
        </p>
      </div>

      <div class="mt-4 flex items-center justify-between border-t border-default pt-3">
        <div class="flex items-center gap-2 text-sm">
          <UIcon
            name="i-lucide-folder-kanban"
            class="size-4 text-muted"
          />
          <span class="font-medium">
            {{ projetosPorPrograma.get(programa.codigo_programa)?.length ?? 0 }}
          </span>
          <span class="text-muted">projetos</span>
        </div>
        <div
          v-if="projetosPorPrograma.get(programa.codigo_programa)?.[0]?.gerente_programa"
          class="flex items-center gap-2 text-sm"
        >
          <UAvatar
            :alt="projetosPorPrograma.get(programa.codigo_programa)?.[0]?.gerente_programa"
            :text="initials(projetosPorPrograma.get(programa.codigo_programa)?.[0]?.gerente_programa)"
            size="2xs"
            class="bg-primary/10 text-primary"
          />
          <span class="truncate text-muted">
            {{ projetosPorPrograma.get(programa.codigo_programa)?.[0]?.gerente_programa }}
          </span>
        </div>
      </div>
    </UCard>
  </div>
</template>
