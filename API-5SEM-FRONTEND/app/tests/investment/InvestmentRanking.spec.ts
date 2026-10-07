import { describe, it, expect } from 'vitest'
import type { ProgramaInvestimento } from '~/types/api'

function getTop3(programas: ProgramaInvestimento[]) {
  return [...programas]
    .sort((a, b) => Number(b.investimento_total) - Number(a.investimento_total))
    .slice(0, 3)
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

function formatBRL(value: string | number) {
  return Number(value).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })
}

const mockProgramas: ProgramaInvestimento[] = [
  { codigo_programa: 'P1', nome_programa: 'Programa Alpha', investimento_total: '500000' },
  { codigo_programa: 'P2', nome_programa: 'Programa Beta', investimento_total: '300000' },
  { codigo_programa: 'P3', nome_programa: 'Programa Gamma', investimento_total: '800000' },
  { codigo_programa: 'P4', nome_programa: 'Programa Delta', investimento_total: '100000' }
]

describe('InvestmentRanking', () => {
  it('retorna no máximo 3 programas', () => {
    // Arrange + Act
    const result = getTop3(mockProgramas)

    // Assert
    expect(result.length).toBeLessThanOrEqual(3)
  })

  it('ordena por maior investimento primeiro', () => {
    // Arrange + Act
    const result = getTop3(mockProgramas)

    // Assert
    expect(result[0]?.nome_programa).toBe('Programa Gamma')
    expect(result[1]?.nome_programa).toBe('Programa Alpha')
    expect(result[2]?.nome_programa).toBe('Programa Beta')
  })

  it('não inclui programas fora do top 3', () => {
    // Arrange + Act
    const result = getTop3(mockProgramas)

    // Assert
    expect(result.find(p => p.nome_programa === 'Programa Delta')).toBeUndefined()
  })

  it('gera iniciais corretamente', () => {
    // Arrange + Act + Assert
    expect(initials('Ana Silva')).toBe('AS')
    expect(initials('Bruno')).toBe('B')
    expect(initials(undefined)).toBe('?')
  })

  it('formata valor em BRL', () => {
    // Arrange + Act
    const result = formatBRL(1000)

    // Assert
    expect(result).toContain('1.000')
    expect(result).toContain('R$')
  })
})
