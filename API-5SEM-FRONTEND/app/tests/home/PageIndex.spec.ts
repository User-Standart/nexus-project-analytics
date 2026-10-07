import { describe, it, expect } from 'vitest'
import type { DimProjeto, FatoExecucao, FatoCompra } from '~/types/api'

function filtrarProjetos(projetos: DimProjeto[], programa: string, status: string) {
  return projetos.filter(p =>
    (programa === 'Todos' || p.nome_programa === programa)
    && (status === 'Todos' || p.status === status)
  )
}

function calcularTotalHoras(execucoes: FatoExecucao[]) {
  return execucoes.reduce((acc, e) => acc + Number(e.horas_trabalhadas), 0)
}

function calcularTotalCompras(compras: FatoCompra[]) {
  return compras.reduce((acc, c) => acc + Number(c.valor_total_pedido), 0)
}

function groupBy(
  items: { sk_projeto: string }[],
  field: string,
  nomeMap: Map<string, string>
) {
  const map = new Map<string, number>()
  for (const item of items) {
    const key = item.sk_projeto
    const val = Number((item as Record<string, string>)[field])
    map.set(key, (map.get(key) ?? 0) + val)
  }
  const labels: string[] = []
  const data: number[] = []
  for (const [sk, total] of map) {
    labels.push(nomeMap.get(sk) ?? `Projeto ${sk}`)
    data.push(total)
  }
  return { labels, data }
}

const mockProjetos: DimProjeto[] = [
  {
    sk_projeto: '1', id_projeto: 'P01', nome_projeto: 'Projeto A', status: 'Em andamento',
    codigo_projeto: 'COD01', codigo_programa: 'PRG1', nome_programa: 'Programa Alpha',
    gerente_programa: 'Ana', responsavel: 'Bruno', data_inicio: '2024-01-01', data_fim_prevista: '2025-01-01'
  },
  {
    sk_projeto: '2', id_projeto: 'P02', nome_projeto: 'Projeto B', status: 'Concluído',
    codigo_projeto: 'COD02', codigo_programa: 'PRG2', nome_programa: 'Programa Beta',
    gerente_programa: 'Carla', responsavel: 'Daniel', data_inicio: '2023-01-01', data_fim_prevista: '2024-01-01'
  }
]

const mockExecucoes: FatoExecucao[] = [
  { sk_fato: '1', sk_projeto: 'P01', sk_tarefa: 'T1', sk_responsavel: 'Bruno', sk_tempo: '2024-01-01', horas_trabalhadas: '8' },
  { sk_fato: '2', sk_projeto: 'P01', sk_tarefa: 'T2', sk_responsavel: 'Bruno', sk_tempo: '2024-01-02', horas_trabalhadas: '4' },
  { sk_fato: '3', sk_projeto: 'P02', sk_tarefa: 'T3', sk_responsavel: 'Daniel', sk_tempo: '2024-01-01', horas_trabalhadas: '6' }
]

const mockCompras: FatoCompra[] = [
  { sk_fato: '1', sk_projeto: 'P01', valor_total_pedido: '1000', valor_alocado_projeto: '800' },
  { sk_fato: '2', sk_projeto: 'P02', valor_total_pedido: '500', valor_alocado_projeto: '400' }
]

describe('PageIndex', () => {
  it('filtra projetos por programa', () => {
    // Arrange + Act
    const result = filtrarProjetos(mockProjetos, 'Programa Alpha', 'Todos')

    // Assert
    expect(result.length).toBe(1)
    expect(result[0]?.nome_projeto).toBe('Projeto A')
  })

  it('filtra projetos por status', () => {
    // Arrange + Act
    const result = filtrarProjetos(mockProjetos, 'Todos', 'Concluído')

    // Assert
    expect(result.length).toBe(1)
    expect(result[0]?.nome_projeto).toBe('Projeto B')
  })

  it('calcula total de horas corretamente', () => {
    // Arrange + Act
    const result = calcularTotalHoras(mockExecucoes)

    // Assert
    expect(result).toBe(18)
  })

  it('calcula total de compras corretamente', () => {
    // Arrange + Act
    const result = calcularTotalCompras(mockCompras)

    // Assert
    expect(result).toBe(1500)
  })

  it('agrupa execuções por projeto com nome correto', () => {
    // Arrange
    const nomeMap = new Map([['P01', 'Projeto A'], ['P02', 'Projeto B']])

    // Act
    const result = groupBy(mockExecucoes, 'horas_trabalhadas', nomeMap)

    // Assert
    expect(result.labels).toContain('Projeto A')
    expect(result.data[result.labels.indexOf('Projeto A')]).toBe(12)
  })

  it('retorna zero para listas vazias', () => {
    expect(calcularTotalHoras([])).toBe(0)
    expect(calcularTotalCompras([])).toBe(0)
  })
})
