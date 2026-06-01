import { describe, it, expect } from 'vitest'
import type { MateriaisPorProjeto } from '~/types/api'

function getTotalProjetos(materiais: MateriaisPorProjeto[]) {
  return new Set(materiais.map(m => m.codigo_projeto)).size
}

function getMediaPorMaterial(materiais: MateriaisPorProjeto[]) {
  if (!materiais.length) return 0
  const total = materiais.reduce((acc, m) => acc + m.quantidade_estoque, 0)
  return Math.round(total / materiais.length)
}

function getMaterialMaisFrequente(materiais: MateriaisPorProjeto[]) {
  if (!materiais.length) return '-'
  const map = new Map<string, number>()
  for (const m of materiais) {
    map.set(m.descricao_material, (map.get(m.descricao_material) ?? 0) + 1)
  }
  return [...map.entries()].sort((a, b) => b[1] - a[1])[0]?.[0] ?? '-'
}

const mockMateriais: MateriaisPorProjeto[] = [
  { codigo_projeto: '1', nome_projeto: 'Projeto A', codigo_material: 'M01', descricao_material: 'Parafuso', quantidade_estoque: 100 },
  { codigo_projeto: '1', nome_projeto: 'Projeto A', codigo_material: 'M02', descricao_material: 'Parafuso', quantidade_estoque: 50 },
  { codigo_projeto: '2', nome_projeto: 'Projeto B', codigo_material: 'M03', descricao_material: 'Porca', quantidade_estoque: 20 },
  { codigo_projeto: '3', nome_projeto: 'Projeto C', codigo_material: 'M04', descricao_material: 'Arruela', quantidade_estoque: 30 }
]

describe('PageMateriais', () => {
  it('conta projetos únicos corretamente', () => {
    // Arrange + Act
    const result = getTotalProjetos(mockMateriais)

    // Assert
    expect(result).toBe(3)
  })

  it('calcula média de estoque por material', () => {
    // Arrange + Act
    const result = getMediaPorMaterial(mockMateriais)

    // Assert
    expect(result).toBe(50)
  })

  it('retorna 0 para lista vazia', () => {
    expect(getMediaPorMaterial([])).toBe(0)
  })

  it('retorna material mais frequente corretamente', () => {
    // Arrange + Act
    const result = getMaterialMaisFrequente(mockMateriais)

    // Assert
    expect(result).toBe('Parafuso')
  })

  it('retorna traço para lista vazia', () => {
    expect(getMaterialMaisFrequente([])).toBe('-')
  })
})
