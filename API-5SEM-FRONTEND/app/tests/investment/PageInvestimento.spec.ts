import { describe, it, expect } from 'vitest'
import type { DimProjeto } from '~/types/api'

function getProjetosPorPrograma(projetos: DimProjeto[]) {
  const map = new Map<string, DimProjeto[]>()
  for (const p of projetos) {
    const lista = map.get(p.codigo_programa) ?? []
    lista.push(p)
    map.set(p.codigo_programa, lista)
  }
  return map
}

const mockProjetos: DimProjeto[] = [
  {
    sk_projeto: '1', id_projeto: 'P01', nome_projeto: 'Projeto A', status: 'Em andamento',
    codigo_projeto: 'COD01', codigo_programa: 'PRG1', nome_programa: 'Programa Alpha',
    gerente_programa: 'Ana', responsavel: 'Bruno', data_inicio: '2024-01-01', data_fim_prevista: '2025-01-01'
  },
  {
    sk_projeto: '2', id_projeto: 'P02', nome_projeto: 'Projeto B', status: 'Concluído',
    codigo_projeto: 'COD02', codigo_programa: 'PRG1', nome_programa: 'Programa Alpha',
    gerente_programa: 'Ana', responsavel: 'Carla', data_inicio: '2023-01-01', data_fim_prevista: '2024-01-01'
  },
  {
    sk_projeto: '3', id_projeto: 'P03', nome_projeto: 'Projeto C', status: 'Planejamento',
    codigo_projeto: 'COD03', codigo_programa: 'PRG2', nome_programa: 'Programa Beta',
    gerente_programa: 'Daniel', responsavel: 'Eva', data_inicio: '2025-01-01', data_fim_prevista: '2026-01-01'
  }
]

describe('PageInvestimento', () => {
  it('agrupa projetos por programa corretamente', () => {
    // Arrange + Act
    const result = getProjetosPorPrograma(mockProjetos)

    // Assert
    expect(result.get('PRG1')?.length).toBe(2)
    expect(result.get('PRG2')?.length).toBe(1)
  })

  it('retorna mapa vazio para lista vazia', () => {
    // Arrange + Act
    const result = getProjetosPorPrograma([])

    // Assert
    expect(result.size).toBe(0)
  })

  it('todos os projetos do programa estão no grupo', () => {
    // Arrange + Act
    const result = getProjetosPorPrograma(mockProjetos)
    const prg1 = result.get('PRG1') ?? []

    // Assert
    expect(prg1.map(p => p.nome_projeto)).toContain('Projeto A')
    expect(prg1.map(p => p.nome_projeto)).toContain('Projeto B')
  })
})
