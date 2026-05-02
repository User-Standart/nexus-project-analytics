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
