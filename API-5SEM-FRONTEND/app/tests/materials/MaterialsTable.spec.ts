import { describe, it, expect } from 'vitest'
import type { MateriaisPorProjeto } from '~/types/api'

function estoqueColor(qtd: number) {
  if (qtd === 0) return 'error'
  if (qtd < 10) return 'warning'
  return 'success'
}

function getProjetos(materiais: MateriaisPorProjeto[]) {
  return ['Todos', ...new Set(materiais.map(m => m.nome_projeto))]
}

function filtrarMateriais(materiais: MateriaisPorProjeto[], filtro: string) {
  return materiais.filter(m => filtro === 'Todos' || m.nome_projeto === filtro)
}

function paginar<T>(items: T[], pagina: number, porPagina: number) {
  const inicio = (pagina - 1) * porPagina
  return items.slice(inicio, inicio + porPagina)
}

function totalPaginas(total: number, porPagina: number) {
  return Math.ceil(total / porPagina)
}

function calcularDetalhe(materiais: MateriaisPorProjeto[], selecionado: MateriaisPorProjeto) {
  const ocorrencias = materiais.filter(x => x.codigo_material === selecionado.codigo_material)
  const totalEstoque = ocorrencias.reduce((acc, x) => acc + x.quantidade_estoque, 0)
  const projetosDistintos = new Set(ocorrencias.map(x => x.codigo_projeto))
  return {
    ocorrencias,
    totalEstoque,
    quantidadeProjetos: projetosDistintos.size
  }
}

const mockMateriais: MateriaisPorProjeto[] = [
  { codigo_projeto: '1', nome_projeto: 'Projeto A', codigo_material: 'M01', descricao_material: 'Parafuso', quantidade_estoque: 100 },
  { codigo_projeto: '2', nome_projeto: 'Projeto B', codigo_material: 'M02', descricao_material: 'Porca', quantidade_estoque: 5 },
  { codigo_projeto: '3', nome_projeto: 'Projeto C', codigo_material: 'M03', descricao_material: 'Arruela', quantidade_estoque: 0 },
  { codigo_projeto: '1', nome_projeto: 'Projeto A', codigo_material: 'M01', descricao_material: 'Parafuso', quantidade_estoque: 50 }
]

describe('MaterialsTable', () => {
  it('retorna error para estoque zero', () => {
    // Arrange
    const qtd = 0

    // Act
    const result = estoqueColor(qtd)

    // Assert
    expect(result).toBe('error')
  })

  it('retorna warning para estoque menor que 10', () => {
    // Arrange
    const qtd = 5

    // Act
    const result = estoqueColor(qtd)

    // Assert
    expect(result).toBe('warning')
  })

  it('retorna success para estoque maior ou igual a 10', () => {
    // Arrange
    const qtd = 10

    // Act
    const result = estoqueColor(qtd)

    // Assert
    expect(result).toBe('success')
  })

  it('lista projetos únicos com Todos no início', () => {
    // Arrange + Act
    const projetos = getProjetos(mockMateriais)

    // Assert
    expect(projetos[0]).toBe('Todos')
    expect(projetos).toContain('Projeto A')
    expect(projetos.filter(p => p === 'Projeto A').length).toBe(1)
  })

  it('filtra Todos retorna todos os materiais', () => {
    // Arrange + Act
    const result = filtrarMateriais(mockMateriais, 'Todos')

    // Assert
    expect(result.length).toBe(4)
  })

  it('filtra por projeto específico', () => {
    // Arrange + Act
    const result = filtrarMateriais(mockMateriais, 'Projeto A')

    // Assert
    expect(result.length).toBe(2)
    expect(result.every(m => m.nome_projeto === 'Projeto A')).toBe(true)
  })

  it('pagina corretamente a primeira página', () => {
    // Arrange + Act
    const result = paginar(mockMateriais, 1, 3)

    // Assert
    expect(result.length).toBe(3)
  })

  it('pagina corretamente a segunda página', () => {
    // Arrange + Act
    const result = paginar(mockMateriais, 2, 3)

    // Assert
    expect(result.length).toBe(1)
  })

  it('calcula total de páginas corretamente', () => {
    expect(totalPaginas(10, 5)).toBe(2)
    expect(totalPaginas(11, 5)).toBe(3)
    expect(totalPaginas(5, 5)).toBe(1)
  })

  it('calcula detalhe do material corretamente', () => {
    // Arrange
    const selecionado = mockMateriais[0] as MateriaisPorProjeto

    // Act
    const detalhe = calcularDetalhe(mockMateriais, selecionado)

    // Assert
    expect(detalhe.totalEstoque).toBe(150)
    expect(detalhe.ocorrencias.length).toBe(2)
    expect(detalhe.quantidadeProjetos).toBe(1)
  })
})
