<script setup lang="ts" generic="T extends Record<string, string>">
type FilterField = {
  key: keyof T & string
  label: string
  options: string[]
}

const props = defineProps<{
  fields: FilterField[]
  modelValue: T
}>()

const emit = defineEmits<{
  'update:modelValue': [value: T]
}>()

function update(key: keyof T & string, value: string) {
  emit('update:modelValue', { ...props.modelValue, [key]: value })
}

function reset() {
  const cleared = { ...props.modelValue }
  for (const k of Object.keys(cleared) as (keyof T)[]) {
    cleared[k] = 'Todos' as T[keyof T]
  }
  emit('update:modelValue', cleared)
}

const activeCount = computed(() =>
  Object.values(props.modelValue).filter(v => v !== 'Todos').length
)
</script>

<template>
  <UCard class="hidden md:block">
    <template #header>
      <div class="flex items-center justify-between">
        <div class="flex items-center gap-2">
          <UIcon
            name="i-lucide-filter"
            class="size-5 text-primary"
          />
          <h3 class="font-semibold">
            Filtros
          </h3>
        </div>
        <UButton
          v-if="activeCount > 0"
          variant="ghost"
          size="sm"
          icon="i-lucide-rotate-ccw"
          @click="reset"
        >
          Limpar
        </UButton>
      </div>
    </template>

    <div class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
      <UFormField
        v-for="f in fields"
        :key="f.key"
        :label="f.label"
        :name="f.key"
      >
        <USelect
          :model-value="modelValue[f.key]"
          :items="f.options"
          :placeholder="f.label"
          class="w-full"
          @update:model-value="(v: string) => update(f.key, v)"
        />
      </UFormField>
    </div>
  </UCard>

  <UDrawer
    title="Filtros"
    description="Filtre os dados do dashboard"
    class="md:hidden"
  >
    <UButton
      block
      color="neutral"
      variant="soft"
      icon="i-lucide-filter"
      trailing-icon="i-lucide-chevron-up"
    >
      Filtros{{ activeCount > 0 ? ` (${activeCount})` : '' }}
    </UButton>

    <template #body>
      <div class="flex flex-col gap-4 pb-4">
        <UFormField
          v-for="f in fields"
          :key="f.key"
          :label="f.label"
          :name="f.key"
        >
          <USelect
            :model-value="modelValue[f.key]"
            :items="f.options"
            :placeholder="f.label"
            class="w-full"
            @update:model-value="(v: string) => update(f.key, v)"
          />
        </UFormField>

        <UButton
          v-if="activeCount > 0"
          variant="ghost"
          icon="i-lucide-rotate-ccw"
          block
          @click="reset"
        >
          Limpar filtros
        </UButton>
      </div>
    </template>
  </UDrawer>
</template>
