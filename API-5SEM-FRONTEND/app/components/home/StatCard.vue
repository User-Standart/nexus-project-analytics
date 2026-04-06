<script setup lang="ts">
defineProps<{
  label: string
  value: string | number
  icon: string
}>()
</script>

<template>
  <UCard>
    <div class="flex items-center justify-between">
      <div>
        <p class="text-sm text-muted">
          {{ label }}
        </p>
        <p class="text-2xl font-bold">
          {{ value }}
        </p>
      </div>
      <UIcon
        :name="icon"
        class="size-8 text-primary"
      />
    </div>
  </UCard>
</template>
