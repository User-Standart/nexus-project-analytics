import { describe, it, expect } from 'vitest'
import type { FatoExecucao } from '~/types/api'

function agruparHorasPorResponsavel(execucoes: FatoExecucao[]) {
  const map = new Map<string, number>()
  for (const e of execucoes) {
    const total = (map.get(e.sk_responsavel) ?? 0) + Number(e.horas_trabalhadas)
    map.set(e.sk_responsavel, total)
  }
  return [...map.entries()]
    .sort((a, b) => b[1] - a[1])
    .slice(0, 10)
    .map(([nome, total]) => ({ nome, total: Number(total.toFixed(1)) }))
}

const mockExecucoes: FatoExecucao[] = [
  { sk_fato: '1', sk_projeto: 'P1', sk_tarefa: 'T1', sk_responsavel: 'Ana', sk_tempo: '2025-01-01', horas_trabalhadas: '8' },
  { sk_fato: '2', sk_projeto: 'P1', sk_tarefa: 'T2', sk_responsavel: 'Ana', sk_tempo: '2025-01-02', horas_trabalhadas: '4' },
  { sk_fato: '3', sk_projeto: 'P2', sk_tarefa: 'T3', sk_responsavel: 'Bruno', sk_tempo: '2025-01-01', horas_trabalhadas: '6' },
  { sk_fato: '4', sk_projeto: 'P2', sk_tarefa: 'T4', sk_responsavel: 'Carla', sk_tempo: '2025-01-01', horas_trabalhadas: '2' }
]

describe('ProductivityBarChart', () => {
  it('agrupa horas corretamente por responsável', () => {
    // Arrange + Act
    const result = agruparHorasPorResponsavel(mockExecucoes)

    // Assert
    const ana = result.find(r => r.nome === 'Ana')
    expect(ana?.total ?? 0).toBe(12)
  })

  it('ordena por maior total de horas primeiro', () => {
    // Arrange + Act
    const result = agruparHorasPorResponsavel(mockExecucoes)

    // Assert
    expect(result[0]?.nome).toBe('Ana')
    expect(result[1]?.nome).toBe('Bruno')
    expect(result[2]?.nome).toBe('Carla')
  })

  it('limita ao top 10 responsáveis', () => {
    // Arrange
    const muitos: FatoExecucao[] = Array.from({ length: 15 }, (_, i) => ({
      sk_fato: String(i),
      sk_projeto: 'P1',
      sk_tarefa: 'T1',
      sk_responsavel: `Responsavel ${i}`,
      sk_tempo: '2025-01-01',
      horas_trabalhadas: String(i + 1)
    }))

    // Act
    const result = agruparHorasPorResponsavel(muitos)

    // Assert
    expect(result.length).toBeLessThanOrEqual(10)
  })

  it('arredonda total para 1 casa decimal', () => {
    // Arrange
    const execucoes: FatoExecucao[] = [
      { sk_fato: '1', sk_projeto: 'P1', sk_tarefa: 'T1', sk_responsavel: 'Ana', sk_tempo: '2025-01-01', horas_trabalhadas: '1.333' },
      { sk_fato: '2', sk_projeto: 'P1', sk_tarefa: 'T2', sk_responsavel: 'Ana', sk_tempo: '2025-01-02', horas_trabalhadas: '1.333' }
    ]

    // Act
    const result = agruparHorasPorResponsavel(execucoes)

    // Assert
    expect(result[0]?.total).toBe(2.7)
  })

  it('retorna vazio para lista vazia', () => {
    // Arrange + Act
    const result = agruparHorasPorResponsavel([])

    // Assert
    expect(result.length).toBe(0)
  })
})
