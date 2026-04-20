export interface DimProjeto {
  sk_projeto: string
  id_projeto: string
  nome_projeto: string
  status: string
}

export interface DimTarefa {
  sk_tarefa: string
  titulo: string
  status: string
  estimativa_horas: string
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
