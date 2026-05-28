import { describe, it, expect } from 'vitest'
import type { FatoExecucao } from '~/types/api'

function getResponsaveis(execucoes: FatoExecucao[]) {
  return ['Todos', ...new Set(execucoes.map(e => e.sk_responsavel))]
}

function filtrarExecucoes(execucoes: FatoExecucao[], filtro: string) {
  return execucoes.filter(e => filtro === 'Todos' || e.sk_responsavel === filtro)
}

function calcularTotalResponsavel(execucoes: FatoExecucao[], responsavel: string) {
  return execucoes
    .filter(x => x.sk_responsavel === responsavel)
    .reduce((acc, x) => acc + Number(x.horas_trabalhadas), 0)
}

function calcularTotalProjeto(execucoes: FatoExecucao[], skProjeto: string) {
  return execucoes
    .filter(x => x.sk_projeto === skProjeto)
    .reduce((acc, x) => acc + Number(x.horas_trabalhadas), 0)
}

function initials(name: string | undefined) {
  if (!name) return '?'
  return name.split(' ').filter(Boolean).slice(0, 2).map(n => n[0]?.toUpperCase() ?? '').join('')
}

function formatDate(date: string) {
  return new Date(date).toLocaleDateString('pt-BR')
}

const mockExecucoes: FatoExecucao[] = [
  { sk_fato: '1', sk_projeto: 'P1', sk_tarefa: 'T1', sk_responsavel: 'Ana', sk_tempo: '2025-01-01', horas_trabalhadas: '8' },
  { sk_fato: '2', sk_projeto: 'P1', sk_tarefa: 'T2', sk_responsavel: 'Ana', sk_tempo: '2025-01-02', horas_trabalhadas: '4' },
  { sk_fato: '3', sk_projeto: 'P2', sk_tarefa: 'T3', sk_responsavel: 'Bruno', sk_tempo: '2025-01-01', horas_trabalhadas: '6' },
  { sk_fato: '4', sk_projeto: 'P2', sk_tarefa: 'T4', sk_responsavel: 'Carla', sk_tempo: '2025-01-01', horas_trabalhadas: '2' }
]

describe('ProductivityTable', () => {
  it('lista responsáveis únicos com Todos no início', () => {
    // Arrange + Act
    const result = getResponsaveis(mockExecucoes)

    // Assert
    expect(result[0]).toBe('Todos')
    expect(result).toContain('Ana')
    expect(result.filter(r => r === 'Ana').length).toBe(1)
  })

  it('filtra Todos retorna todas as execuções', () => {
    // Arrange + Act
    const result = filtrarExecucoes(mockExecucoes, 'Todos')

    // Assert
    expect(result.length).toBe(4)
  })

  it('filtra por responsável específico', () => {
    // Arrange + Act
    const result = filtrarExecucoes(mockExecucoes, 'Ana')

    // Assert
    expect(result.length).toBe(2)
    expect(result.every(e => e.sk_responsavel === 'Ana')).toBe(true)
  })

  it('calcula total de horas por responsável', () => {
    // Arrange + Act
    const result = calcularTotalResponsavel(mockExecucoes, 'Ana')

    // Assert
    expect(result).toBe(12)
  })

  it('calcula total de horas por projeto', () => {
    // Arrange + Act
    const result = calcularTotalProjeto(mockExecucoes, 'P1')

    // Assert
    expect(result).toBe(12)
  })

  it('gera iniciais corretamente', () => {
    expect(initials('Ana Silva')).toBe('AS')
    expect(initials('Bruno')).toBe('B')
    expect(initials(undefined)).toBe('?')
  })

  it('formata data corretamente', () => {
    // Arrange + Act
    const result = formatDate('2025-01-15')

    // Assert
    expect(result).toContain('2025')
  })
})
