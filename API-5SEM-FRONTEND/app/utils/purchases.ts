import type { Purchase, StatusCount } from '~/types/api'

export type UiColor = 'primary' | 'secondary' | 'success' | 'info' | 'warning' | 'error' | 'neutral'

export interface PurchaseFilters {
  tipo: string
  status: string
}

export function filterPurchases(purchases: Purchase[], filtros: PurchaseFilters): Purchase[] {
  return purchases.filter((p) => {
    const matchTipo = filtros.tipo === 'Todos' || p.type === filtros.tipo
    const matchStatus = filtros.status === 'Todos' || p.status === filtros.status
    return matchTipo && matchStatus
  })
}

export function purchaseStatusOptions(purchases: Purchase[]): string[] {
  return ['Todos', ...new Set(purchases.map(p => p.status))]
}

export interface PurchaseMetricsSummary {
  totalSC: number
  totalPC: number
  avgDurationPC: number
  atrasados: number
}

export function computeMetrics(purchases: Purchase[]): PurchaseMetricsSummary {
  let totalSC = 0
  let totalPC = 0
  let atrasados = 0
  let somaDuracao = 0
  let countDuracao = 0

  for (const p of purchases) {
    if (p.type === 'SC') {
      totalSC++
    } else if (p.type === 'PC') {
      totalPC++
      if (typeof p.duracao_dias === 'number') {
        somaDuracao += p.duracao_dias
        countDuracao++
      }
    }
    if (p.atrasado) {
      atrasados++
    }
  }

  return {
    totalSC,
    totalPC,
    avgDurationPC: countDuracao > 0 ? somaDuracao / countDuracao : 0,
    atrasados
  }
}

export function statusCounts(purchases: Purchase[]): StatusCount[] {
  const map = new Map<string, number>()
  for (const p of purchases) {
    map.set(p.status, (map.get(p.status) ?? 0) + 1)
  }
  return [...map.entries()]
    .map(([status, count]) => ({ status, count }))
    .sort((a, b) => b.count - a.count)
}

export function formatDuration(days: number | null | undefined): string {
  if (typeof days !== 'number') {
    return '-'
  }
  return `${days} ${days === 1 ? 'dia' : 'dias'}`
}

export function tipoColor(tipo: string): UiColor {
  return tipo === 'PC' ? 'primary' : 'neutral'
}

export function statusColor(status: string): UiColor {
  switch (status) {
    case 'Entregue':
    case 'Concluído':
    case 'Concluido':
    case 'Aprovado':
    case 'Aprovada':
      return 'success'
    case 'Enviado':
    case 'Parcialmente Entregue':
    case 'Em andamento':
    case 'Em processamento':
      return 'info'
    case 'Aberto':
    case 'Pendente':
      return 'warning'
    case 'Cancelado':
    case 'Cancelada':
    case 'Rejeitada':
    case 'Rejeitado':
      return 'error'
    default:
      return 'neutral'
  }
}
