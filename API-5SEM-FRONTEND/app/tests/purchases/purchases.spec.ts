import { describe, it, expect } from 'vitest'
import type { Purchase } from '~/types/api'
import {
  filterPurchases,
  purchaseStatusOptions,
  computeMetrics,
  statusCounts,
  formatDuration,
  statusColor,
  tipoColor
} from '../../utils/purchases'

const mockPurchases: Purchase[] = [
  { id: 1, type: 'SC', numero: 'SC-001', status: 'Aberto', data_criacao: '2026-01-10' },
  { id: 2, type: 'SC', numero: 'SC-002', status: 'Aprovado', data_criacao: '2026-01-12' },
  { id: 3, type: 'PC', numero: 'PC-001', status: 'Entregue', data_criacao: '2026-01-05', data_previsao_entrega: '2026-01-20', duracao_dias: 15, atrasado: false },
  { id: 4, type: 'PC', numero: 'PC-002', status: 'Aberto', data_criacao: '2026-01-08', data_previsao_entrega: '2026-01-15', duracao_dias: 25, atrasado: true }
]

describe('filterPurchases', () => {
  it('retorna todos quando tipo e status são Todos', () => {
    // Arrange + Act
    const result = filterPurchases(mockPurchases, { tipo: 'Todos', status: 'Todos' })

    // Assert
    expect(result.length).toBe(4)
  })

  it('filtra por tipo SC', () => {
    // Arrange + Act
    const result = filterPurchases(mockPurchases, { tipo: 'SC', status: 'Todos' })

    // Assert
    expect(result.length).toBe(2)
    expect(result.every(p => p.type === 'SC')).toBe(true)
  })

  it('filtra por status específico', () => {
    // Arrange + Act
    const result = filterPurchases(mockPurchases, { tipo: 'Todos', status: 'Aberto' })

    // Assert
    expect(result.length).toBe(2)
    expect(result.every(p => p.status === 'Aberto')).toBe(true)
  })

  it('combina filtro de tipo e status', () => {
    // Arrange + Act
    const result = filterPurchases(mockPurchases, { tipo: 'PC', status: 'Aberto' })

    // Assert
    expect(result.length).toBe(1)
    expect(result[0]?.numero).toBe('PC-002')
  })
})

describe('purchaseStatusOptions', () => {
  it('lista status únicos com Todos no início', () => {
    // Arrange + Act
    const result = purchaseStatusOptions(mockPurchases)

    // Assert
    expect(result[0]).toBe('Todos')
    expect(result).toContain('Aberto')
    expect(result.filter(s => s === 'Aberto').length).toBe(1)
  })

  it('retorna apenas Todos para lista vazia', () => {
    expect(purchaseStatusOptions([])).toEqual(['Todos'])
  })
})

describe('computeMetrics', () => {
  it('conta SC e PC corretamente', () => {
    // Arrange + Act
    const result = computeMetrics(mockPurchases)

    // Assert
    expect(result.totalSC).toBe(2)
    expect(result.totalPC).toBe(2)
  })

  it('calcula duração média apenas dos PC', () => {
    // Arrange + Act
    const result = computeMetrics(mockPurchases)

    // Assert: (15 + 25) / 2 = 20
    expect(result.avgDurationPC).toBe(20)
  })

  it('conta pedidos atrasados', () => {
    // Arrange + Act
    const result = computeMetrics(mockPurchases)

    // Assert
    expect(result.atrasados).toBe(1)
  })

  it('zera métricas para lista vazia', () => {
    // Arrange + Act
    const result = computeMetrics([])

    // Assert
    expect(result.totalSC).toBe(0)
    expect(result.totalPC).toBe(0)
    expect(result.avgDurationPC).toBe(0)
    expect(result.atrasados).toBe(0)
  })
})

describe('statusCounts', () => {
  it('agrupa contagem por status', () => {
    // Arrange + Act
    const result = statusCounts(mockPurchases)

    // Assert
    const aberto = result.find(s => s.status === 'Aberto')
    expect(aberto?.count).toBe(2)
  })

  it('ordena do maior para o menor', () => {
    // Arrange + Act
    const result = statusCounts(mockPurchases)

    // Assert
    expect(result[0]?.count).toBeGreaterThanOrEqual(result[1]?.count ?? 0)
  })

  it('retorna vazio para lista vazia', () => {
    expect(statusCounts([])).toEqual([])
  })
})

describe('formatDuration', () => {
  it('formata plural', () => {
    expect(formatDuration(15)).toBe('15 dias')
  })

  it('formata singular', () => {
    expect(formatDuration(1)).toBe('1 dia')
  })

  it('retorna traço para nulo ou indefinido', () => {
    expect(formatDuration(null)).toBe('-')
    expect(formatDuration(undefined)).toBe('-')
  })
})

describe('statusColor', () => {
  it('retorna success para entregue e aprovada', () => {
    expect(statusColor('Entregue')).toBe('success')
    expect(statusColor('Aprovada')).toBe('success')
  })

  it('retorna error para cancelada/cancelado e rejeitada', () => {
    expect(statusColor('Cancelada')).toBe('error')
    expect(statusColor('Cancelado')).toBe('error')
    expect(statusColor('Rejeitada')).toBe('error')
  })

  it('retorna warning para aberto e pendente', () => {
    expect(statusColor('Aberto')).toBe('warning')
    expect(statusColor('Pendente')).toBe('warning')
  })

  it('retorna info para enviado e parcialmente entregue', () => {
    expect(statusColor('Enviado')).toBe('info')
    expect(statusColor('Parcialmente Entregue')).toBe('info')
  })

  it('retorna neutral para status desconhecido', () => {
    expect(statusColor('Qualquer')).toBe('neutral')
  })
})

describe('tipoColor', () => {
  it('retorna primary para PC', () => {
    expect(tipoColor('PC')).toBe('primary')
  })

  it('retorna neutral para SC', () => {
    expect(tipoColor('SC')).toBe('neutral')
  })
})
