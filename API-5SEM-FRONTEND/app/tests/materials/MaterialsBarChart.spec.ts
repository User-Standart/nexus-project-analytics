import { describe, it, expect } from 'vitest'
import type { MateriaisPorProjeto } from '~/types/api'

function agruparEstoquePorProjeto(materiais: MateriaisPorProjeto[]) {
  const map = new Map<string, number>()
  for (const m of materiais) {
    map.set(m.nome_projeto, (map.get(m.nome_projeto) ?? 0) + m.quantidade_estoque)
  }
  return [...map.entries()]
    .sort((a, b) => b[1] - a[1])
    .slice(0, 10)
}

const mockMateriais: MateriaisPorProjeto[] = [
  { codigo_projeto: '1', nome_projeto: 'Projeto A', codigo_material: 'M01', descricao_material: 'Parafuso', quantidade_estoque: 100 },
  { codigo_projeto: '1', nome_projeto: 'Projeto A', codigo_material: 'M02', descricao_material: 'Porca', quantidade_estoque: 50 },
  { codigo_projeto: '2', nome_projeto: 'Projeto B', codigo_material: 'M03', descricao_material: 'Arruela', quantidade_estoque: 200 },
  { codigo_projeto: '3', nome_projeto: 'Projeto C', codigo_material: 'M04', descricao_material: 'Pino', quantidade_estoque: 30 }
]

describe('MaterialsBarChart', () => {
  it('agrupa estoque corretamente por projeto', () => {
    // Arrange + Act
    const result = agruparEstoquePorProjeto(mockMateriais)

    // Assert
    const projetoA = result.find(([nome]) => nome === 'Projeto A')
    expect(projetoA?.[1] ?? 0).toBe(150)
  })

  it('ordena por maior estoque primeiro', () => {
    // Arrange + Act
    const result = agruparEstoquePorProjeto(mockMateriais)

    // Assert
    expect(result[0]?.[0]).toBe('Projeto B')
    expect(result[1]?.[0]).toBe('Projeto A')
    expect(result[2]?.[0]).toBe('Projeto C')
  })

  it('limita ao top 10 projetos', () => {
    // Arrange
    const muitos: MateriaisPorProjeto[] = Array.from({ length: 15 }, (_, i) => ({
      codigo_projeto: String(i),
      nome_projeto: `Projeto ${i}`,
      codigo_material: `M${i}`,
      descricao_material: `Material ${i}`,
      quantidade_estoque: i + 1
    }))

    // Act
    const result = agruparEstoquePorProjeto(muitos)

    // Assert
    expect(result.length).toBeLessThanOrEqual(10)
  })

  it('retorna vazio para lista vazia', () => {
    // Arrange + Act
    const result = agruparEstoquePorProjeto([])

    // Assert
    expect(result.length).toBe(0)
  })
})
