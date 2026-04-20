<script setup lang="ts">
import type { ProgramaInvestimento } from '~/types/api'

const props = defineProps<{
  programas: ProgramaInvestimento[]
}>()

const top3 = computed(() =>
  [...props.programas]
    .sort((a, b) => Number(b.investimento_total) - Number(a.investimento_total))
    .slice(0, 3)
)
</script>

<template>
  <div class="grid grid-cols-1 gap-4 sm:grid-cols-3">
    <UCard
      v-for="(programa, index) in top3"
      :key="programa.codigo_programa"
    >
      <div class="flex flex-col items-center gap-2 py-2 text-center">
        <UIcon
          name="i-lucide-trophy"
          :class="[index === 0 ? 'text-yellow-400' : index === 1 ? 'text-slate-400' : 'text-amber-700', 'size-10']"
        />
        <p class="text-2xl font-extrabold text-primary">
          {{ programa.nome_programa }}
        </p>
        <p class="text-lg font-bold">
          {{ Number(programa.investimento_total).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' }) }}
        </p>
      </div>
    </UCard>
  </div>
</template>
