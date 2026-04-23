<script setup lang="ts">
import type { NavigationMenuItem } from '@nuxt/ui'

const items: NavigationMenuItem[][] = [
  [
    {
      label: 'Home',
      icon: 'i-lucide-house',
      to: '/'
    },
    {
      label: 'Investimentos',
      icon: 'i-lucide-trending-up',
      to: '/investimento'
    }
    // {
    //   label: 'Customers',
    //   icon: 'i-lucide-users',
    //   to: '/customers'
    // },
    // {
    //   label: 'Settings',
    //   icon: 'i-lucide-settings',
    //   to: '/settings'
    // }
  ]
  // [
  //   {
  //     label: 'Help',
  //     icon: 'i-lucide-circle-help',
  //     to: '/help'
  //   }
  // ]
]
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
    </UDashboardSidebar>

    <slot />
  </UDashboardGroup>
</template>
