import { describe, it, expect } from 'vitest'
import type { DimProjeto, FatoExecucao, FatoCompra } from '~/types/api'

function statusColor(status: string) {
  if (status === 'Concluído') return 'success'
  if (status === 'Em andamento') return 'info'
  if (status === 'Planejamento') return 'warning'
  if (status === 'Suspenso') return 'error'
  return 'neutral'
}

function filtrarProjetos(projetos: DimProjeto[], programa: string, status: string) {
  return projetos.filter((p) => {
    const matchPrograma = programa === 'Todos' || p.nome_programa === programa
    const matchStatus = status === 'Todos' || p.status === status
    return matchPrograma && matchStatus
  })
}

function calcularProgresso(dataInicio: string, dataFim: string, hoje: Date) {
  const inicio = new Date(dataInicio).getTime()
  const fim = new Date(dataFim).getTime()
  const duracaoTotal = fim - inicio
  const decorrido = Math.max(0, hoje.getTime() - inicio)
  return duracaoTotal > 0 ? Math.min(100, Math.round((decorrido / duracaoTotal) * 100)) : 0
}

function calcularTotalHoras(execucoes: FatoExecucao[], skProjeto: string) {
  return execucoes
    .filter(e => e.sk_projeto === skProjeto)
    .reduce((acc, e) => acc + Number(e.horas_trabalhadas), 0)
}

function calcularTotalCompras(compras: FatoCompra[], skProjeto: string) {
  return compras
    .filter(c => c.sk_projeto === skProjeto)
    .reduce((acc, c) => acc + Number(c.valor_total_pedido), 0)
}

function initials(name: string | undefined) {
  if (!name) return '?'
  return name
    .split(' ')
    .filter(Boolean)
    .slice(0, 2)
    .map(n => n[0]?.toUpperCase() ?? '')
    .join('')
}

const mockProjetos: DimProjeto[] = [
  {
    sk_projeto: '1', id_projeto: 'P01', nome_projeto: 'Projeto A', status: 'Em andamento',
    codigo_projeto: 'COD01', codigo_programa: 'PRG1', nome_programa: 'Programa Alpha',
    gerente_programa: 'Ana Silva', responsavel: 'Bruno Costa',
    data_inicio: '2024-01-01', data_fim_prevista: '2025-01-01'
  },
  {
    sk_projeto: '2', id_projeto: 'P02', nome_projeto: 'Projeto B', status: 'Concluído',
    codigo_projeto: 'COD02', codigo_programa: 'PRG2', nome_programa: 'Programa Beta',
    gerente_programa: 'Carla Lima', responsavel: 'Daniel Souza',
    data_inicio: '2023-01-01', data_fim_prevista: '2024-01-01'
  },
  {
    sk_projeto: '3', id_projeto: 'P03', nome_projeto: 'Projeto C', status: 'Planejamento',
    codigo_projeto: 'COD03', codigo_programa: 'PRG1', nome_programa: 'Programa Alpha',
    gerente_programa: 'Ana Silva', responsavel: 'Eva Torres',
    data_inicio: '2025-01-01', data_fim_prevista: '2026-01-01'
  }
]

describe('InvestmentTable', () => {
  it('retorna success para status Concluído', () => {
    expect(statusColor('Concluído')).toBe('success')
  })

  it('retorna info para status Em andamento', () => {
    expect(statusColor('Em andamento')).toBe('info')
  })

  it('retorna warning para status Planejamento', () => {
    expect(statusColor('Planejamento')).toBe('warning')
  })

  it('retorna neutral para status desconhecido', () => {
    expect(statusColor('Outro')).toBe('neutral')
  })

  it('filtra por programa específico', () => {
    // Arrange + Act
    const result = filtrarProjetos(mockProjetos, 'Programa Alpha', 'Todos')

    // Assert
    expect(result.length).toBe(2)
    expect(result.every(p => p.nome_programa === 'Programa Alpha')).toBe(true)
  })

  it('filtra por status específico', () => {
    // Arrange + Act
    const result = filtrarProjetos(mockProjetos, 'Todos', 'Concluído')

    // Assert
    expect(result.length).toBe(1)
    expect(result[0]?.nome_projeto).toBe('Projeto B')
  })

  it('filtra por programa e status combinados', () => {
    // Arrange + Act
    const result = filtrarProjetos(mockProjetos, 'Programa Alpha', 'Em andamento')

    // Assert
    expect(result.length).toBe(1)
    expect(result[0]?.nome_projeto).toBe('Projeto A')
  })

  it('calcula progresso entre 0 e 100', () => {
    // Arrange
    const hoje = new Date('2024-07-01')

    // Act
    const result = calcularProgresso('2024-01-01', '2025-01-01', hoje)

    // Assert
    expect(result).toBeGreaterThanOrEqual(0)
    expect(result).toBeLessThanOrEqual(100)
  })

  it('calcula total de horas por projeto', () => {
    // Arrange
    const execucoes: FatoExecucao[] = [
      { sk_fato: '1', sk_projeto: '1', sk_tarefa: 'T1', sk_responsavel: 'Ana', sk_tempo: '2024-01-01', horas_trabalhadas: '8' },
      { sk_fato: '2', sk_projeto: '1', sk_tarefa: 'T2', sk_responsavel: 'Bruno', sk_tempo: '2024-01-02', horas_trabalhadas: '4' },
      { sk_fato: '3', sk_projeto: '2', sk_tarefa: 'T3', sk_responsavel: 'Carla', sk_tempo: '2024-01-01', horas_trabalhadas: '6' }
    ]

    // Act
    const result = calcularTotalHoras(execucoes, '1')

    // Assert
    expect(result).toBe(12)
  })

  it('calcula total de compras por projeto', () => {
    // Arrange
    const compras: FatoCompra[] = [
      { sk_fato: '1', sk_projeto: '1', valor_total_pedido: '1000', valor_alocado_projeto: '800' },
      { sk_fato: '2', sk_projeto: '1', valor_total_pedido: '500', valor_alocado_projeto: '400' }
    ]

    // Act
    const result = calcularTotalCompras(compras, '1')

    // Assert
    expect(result).toBe(1500)
  })

  it('gera iniciais corretamente', () => {
    expect(initials('Ana Silva')).toBe('AS')
    expect(initials('Bruno')).toBe('B')
    expect(initials(undefined)).toBe('?')
  })
})
