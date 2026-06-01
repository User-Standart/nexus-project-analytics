<script setup lang="ts">
import { ref } from 'vue'
import type { AuthFormField, FormSubmitEvent } from '@nuxt/ui'

const { login } = useAuth()

const fields: AuthFormField[] = [
  {
    name: 'email',
    type: 'email',
    label: 'E-mail',
    placeholder: 'seu@email.com',
    required: true
  },
  {
    name: 'senha',
    type: 'password',
    label: 'Senha',
    placeholder: '••••••••',
    required: true
  }
]

const loading = ref(false)
const erro = ref('')

async function onSubmit(event: FormSubmitEvent<{ email: string, senha: string }>) {
  erro.value = ''
  loading.value = true
  try {
    const res = await login(event.data.email, event.data.senha)
    await navigateTo(res.usuario.role === 'compras' ? '/pedidos' : '/')
  } catch {
    erro.value = 'E-mail ou senha inválidos.'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="flex min-h-screen items-center justify-center overflow-hidden bg-default p-4">
    <UPageCard class="relative z-10 w-full max-w-md bg-default/80 backdrop-blur-xl">
      <UAuthForm
        :fields="fields"
        title="Nexus Dashboard"
        description="Acesse sua conta para continuar"
        icon="i-lucide-lock"
        :submit="{ label: 'Entrar', icon: 'i-lucide-log-in' }"
        :loading="loading"
        @submit="onSubmit"
      >
        <template #validation>
          <UAlert
            v-if="erro"
            color="error"
            variant="soft"
            :title="erro"
            icon="i-lucide-triangle-alert"
          />
        </template>
      </UAuthForm>
    </UPageCard>
  </div>
</template>
