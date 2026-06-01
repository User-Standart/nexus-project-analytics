export interface DimProjeto {
  sk_projeto: string
  id_projeto: string
  nome_projeto: string
  status: string
}

export interface DimTarefa {
  sk_tarefa: string
  id_tarefa: string
  codigo_tarefa: string
  titulo: string
  status: string
  estimativa_horas: string
  data_inicio: string
  data_fim_prevista: string
}

export interface FatoExecucao {
  sk_fato: string
  sk_projeto: string
  horas_trabalhadas: string
}

export interface FatoCompra {
  sk_fato: string
  sk_projeto: string
  valor_total_pedido: string
  valor_alocado_projeto: string
}

export interface ProgramaInvestimento {
  codigo_programa: string
  nome_programa: string
  investimento_total: string
}

export interface DimProjeto {
  sk_projeto: string
  id_projeto: string
  nome_projeto: string
  status: string
  codigo_projeto: string
  codigo_programa: string
  nome_programa: string
  gerente_programa: string
  responsavel: string
  data_inicio: string
  data_fim_prevista: string
}

export interface MateriaisPorProjeto {
  codigo_projeto: string
  nome_projeto: string
  codigo_material: string
  descricao_material: string
  quantidade_estoque: number
}

export interface FatoExecucao {
  sk_fato: string
  sk_projeto: string
  sk_tarefa: string
  sk_responsavel: string
  sk_tempo: string
  horas_trabalhadas: string
}

export interface TempoGasto {
  total_tempo_gasto: number
}

// Pedido de compra unificado: Solicitação de Compra (SC) ou Pedido de Compra (PC).
export interface Purchase {
  id: number
  type: 'SC' | 'PC'
  numero: string
  status: string
  data_criacao: string
  data_previsao_entrega?: string | null
  duracao_dias?: number | null
  atrasado?: boolean | null
}

export interface StatusCount {
  status: string
  count: number
}

export interface PurchaseMetrics {
  total_purchases: number
  total_sc: number
  total_pc: number
  average_duration_pc: number
  status_counts: StatusCount[]
}
