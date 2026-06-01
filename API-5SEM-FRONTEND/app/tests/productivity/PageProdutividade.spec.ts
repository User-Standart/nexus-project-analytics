import { describe, it, expect } from 'vitest'
import type { FatoExecucao } from '~/types/api'

function getResponsavelMaisProdutivo(execucoes: FatoExecucao[]) {
  if (!execucoes.length) return '-'
  const map = new Map<string, number>()
  for (const e of execucoes) {
    map.set(e.sk_responsavel, (map.get(e.sk_responsavel) ?? 0) + Number(e.horas_trabalhadas))
  }
  return [...map.entries()].sort((a, b) => b[1] - a[1])[0]?.[0] ?? '-'
}

function getMediaPorExecucao(execucoes: FatoExecucao[]) {
  if (!execucoes.length) return 0
  const total = execucoes.reduce((acc, e) => acc + Number(e.horas_trabalhadas), 0)
  return Number((total / execucoes.length).toFixed(1))
}

const mockExecucoes: FatoExecucao[] = [
  { sk_fato: '1', sk_projeto: 'P1', sk_tarefa: 'T1', sk_responsavel: 'Ana', sk_tempo: '2025-01-01', horas_trabalhadas: '10' },
  { sk_fato: '2', sk_projeto: 'P1', sk_tarefa: 'T2', sk_responsavel: 'Ana', sk_tempo: '2025-01-02', horas_trabalhadas: '10' },
  { sk_fato: '3', sk_projeto: 'P2', sk_tarefa: 'T3', sk_responsavel: 'Bruno', sk_tempo: '2025-01-01', horas_trabalhadas: '6' }
]

describe('PageProdutividade', () => {
  it('retorna responsável mais produtivo corretamente', () => {
    // Arrange + Act
    const result = getResponsavelMaisProdutivo(mockExecucoes)

    // Assert
    expect(result).toBe('Ana')
  })

  it('retorna traço para lista vazia', () => {
    expect(getResponsavelMaisProdutivo([])).toBe('-')
  })

  it('calcula média de horas por execução corretamente', () => {
    // Arrange + Act
    const result = getMediaPorExecucao(mockExecucoes)

    // Assert
    expect(result).toBe(8.7)
  })

  it('retorna 0 para lista vazia', () => {
    expect(getMediaPorExecucao([])).toBe(0)
  })
})
