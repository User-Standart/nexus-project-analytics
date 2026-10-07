<script setup lang="ts">
defineProps<{
  label: string
  value: string | number
  icon: string
  hint?: string
  iconClass?: string
}>()
</script>

<template>
  <UCard :ui="{ body: 'p-4' }">
    <div class="flex items-start justify-between gap-2">
      <div class="min-w-0 flex-1">
        <p class="truncate text-xs uppercase tracking-wide text-muted">
          {{ label }}
        </p>
        <p class="mt-1 truncate text-2xl font-bold">
          {{ value }}
        </p>
        <p
          v-if="hint"
          class="mt-0.5 truncate text-xs text-muted"
        >
          {{ hint }}
        </p>
      </div>
      <UIcon
        :name="icon"
        class="size-6 shrink-0 text-primary"
        :class="iconClass"
      />
    </div>
    <slot />
  </UCard>
</template>
