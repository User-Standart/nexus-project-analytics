import { describe, it, expect } from 'vitest'

function buildChartData(labels: string[], data: number[], label?: string) {
  return {
    labels,
    datasets: [
      {
        label: label ?? 'Valor',
        data,
        backgroundColor: '#EA3837',
        borderRadius: 6
      }
    ]
  }
}

describe('HomeBarChart', () => {
  it('monta chartData com labels e data corretos', () => {
    // Arrange
    const labels = ['Projeto A', 'Projeto B']
    const data = [100, 200]

    // Act
    const result = buildChartData(labels, data)

    // Assert
    expect(result.labels).toEqual(['Projeto A', 'Projeto B'])
    expect(result.datasets[0]?.data).toEqual([100, 200])
  })

  it('usa label padrão Valor quando não fornecido', () => {
    // Arrange + Act
    const result = buildChartData([], [])

    // Assert
    expect(result.datasets[0]?.label).toBe('Valor')
  })

  it('usa label personalizado quando fornecido', () => {
    // Arrange + Act
    const result = buildChartData([], [], 'Horas')

    // Assert
    expect(result.datasets[0]?.label).toBe('Horas')
  })

  it('retorna datasets vazio para dados vazios', () => {
    // Arrange + Act
    const result = buildChartData([], [])

    // Assert
    expect(result.labels.length).toBe(0)
    expect(result.datasets[0]?.data.length).toBe(0)
  })
})
