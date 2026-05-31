import { describe, it, expect } from 'vitest'

interface DimTarefa {
  sk_tarefa: string
  titulo: string
}

function filtrarTarefas(
  tarefas: DimTarefa[],
  pesquisa: string
) {
  return tarefas.filter(t =>
    t.titulo
      .toLowerCase()
      .includes(pesquisa.toLowerCase())
  )
}

describe('Task Search', () => {
  it('should return matching tasks', () => {
    // Arrange
    const tarefas = [
      {
        sk_tarefa: '1',
        titulo: 'Teste de isolação'
      },
      {
        sk_tarefa: '2',
        titulo: 'Validação EMC'
      }
    ]

    // Act
    const resultado = filtrarTarefas(
      tarefas,
      'isolação'
    )

    // Assert
    expect(resultado).toHaveLength(1)
    expect(resultado[0]?.titulo)
      .toBe('Teste de isolação')
  })

  it('should return empty array when no task matches', () => {
    // Arrange
    const tarefas = [
      {
        sk_tarefa: '1',
        titulo: 'Teste de isolação'
      }
    ]

    // Act
    const resultado = filtrarTarefas(
      tarefas,
      'microcontrolador'
    )

    // Assert
    expect(resultado).toEqual([])
  })
})
