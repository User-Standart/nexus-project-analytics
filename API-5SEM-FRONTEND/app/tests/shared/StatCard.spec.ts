import { describe, it, expect } from 'vitest'

// Simula a lógica de formatação de valores do dashboard
function formatValue(value: string | number): string {
  return String(value)
}

function isValidIcon(icon: string): boolean {
  return icon.startsWith('i-')
}

describe('Dashboard utils', () => {
  it('formats numeric value to string', () => {
    expect(formatValue(42)).toBe('42')
  })

  it('formats string value correctly', () => {
    expect(formatValue('120.5h')).toBe('120.5h')
  })

  it('formats currency string correctly', () => {
    expect(formatValue('R$ 1.000,00')).toBe('R$ 1.000,00')
  })

  it('validates icon name format', () => {
    expect(isValidIcon('i-lucide-folder-kanban')).toBe(true)
  })

  it('rejects invalid icon name', () => {
    expect(isValidIcon('folder-kanban')).toBe(false)
  })
})
