<script setup lang="ts">
import { computed } from 'vue'
import type { NavigationMenuItem } from '@nuxt/ui'

const { user, role, logout } = useAuth()

const pedidosItem: NavigationMenuItem = {
  label: 'Pedidos de Compra',
  icon: 'i-lucide-shopping-cart',
  to: '/pedidos'
}

const dashboardItems: NavigationMenuItem[] = [
  {
    label: 'Home',
    icon: 'i-lucide-house',
    to: '/'
  },
  {
    label: 'Investimentos',
    icon: 'i-lucide-trending-up',
    to: '/investimento'
  },
  {
    label: 'Materiais',
    icon: 'i-lucide-package',
    to: '/materiais'
  },
  {
    label: 'Horas Trabalhadas',
    icon: 'i-lucide-activity',
    to: '/horastrabalhadas'
  },
  pedidosItem
]

// Perfil "compras" enxerga apenas a tela de Pedidos; admin vê tudo.
const items = computed<NavigationMenuItem[][]>(() =>
  role.value === 'compras' ? [[pedidosItem]] : [dashboardItems]
)
</script>

<template>
  <UDashboardGroup>
    <UDashboardSidebar
      collapsible
      resizable
      :min-size="15"
      :default-size="20"
      :max-size="30"
    >
      <template #header="{ collapsed }">
        <div
          class="flex items-center gap-2 p-2"
          :class="collapsed ? 'justify-center' : ''"
        >
          <NuxtLink to="/">
            <AppLogo
              v-if="!collapsed"
              class="h-6 w-auto"
            />
            <UIcon
              v-else
              name="i-lucide-layout-dashboard"
              class="size-6 text-primary"
            />
          </NuxtLink>
        </div>
      </template>

      <template #default="{ collapsed }">
        <UNavigationMenu
          :collapsed="collapsed"
          orientation="vertical"
          :items="items"
          class="px-2"
        />
      </template>

      <template #footer="{ collapsed }">
        <div
          class="flex w-full items-center gap-2"
          :class="collapsed ? 'justify-center' : 'justify-between'"
        >
          <div
            v-if="!collapsed && user"
            class="min-w-0"
          >
            <p class="truncate text-sm font-medium">
              {{ user.nome }}
            </p>
            <p class="truncate text-xs text-muted capitalize">
              {{ user.role }}
            </p>
          </div>
          <UButton
            icon="i-lucide-log-out"
            color="neutral"
            variant="ghost"
            :label="collapsed ? undefined : 'Sair'"
            aria-label="Sair"
            @click="logout"
          />
        </div>
      </template>
    </UDashboardSidebar>

    <slot />
  </UDashboardGroup>
</template>
