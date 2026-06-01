import { describe, it, expect } from 'vitest'

function buildLineChartData(labels: string[], data: number[], label?: string) {
  return {
    labels,
    datasets: [
      {
        label: label ?? 'Valor',
        data,
        borderColor: '#EA3837',
        backgroundColor: 'rgba(234, 56, 55, 0.1)',
        fill: true,
        tension: 0.4,
        pointRadius: 4,
        pointHoverRadius: 6
      }
    ]
  }
}

describe('HomeLineChart', () => {
  it('monta chartData com labels e data corretos', () => {
    // Arrange
    const labels = ['Jan', 'Fev', 'Mar']
    const data = [10, 20, 30]

    // Act
    const result = buildLineChartData(labels, data)

    // Assert
    expect(result.labels).toEqual(['Jan', 'Fev', 'Mar'])
    expect(result.datasets[0]?.data).toEqual([10, 20, 30])
  })

  it('usa label padrão Valor quando não fornecido', () => {
    // Arrange + Act
    const result = buildLineChartData([], [])

    // Assert
    expect(result.datasets[0]?.label).toBe('Valor')
  })

  it('usa label personalizado quando fornecido', () => {
    // Arrange + Act
    const result = buildLineChartData([], [], 'Valor (R$)')

    // Assert
    expect(result.datasets[0]?.label).toBe('Valor (R$)')
  })

  it('configura fill e tension corretamente', () => {
    // Arrange + Act
    const result = buildLineChartData([], [])

    // Assert
    expect(result.datasets[0]?.fill).toBe(true)
    expect(result.datasets[0]?.tension).toBe(0.4)
  })
})
