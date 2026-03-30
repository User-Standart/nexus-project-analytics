import polars as pl

# sk=0 é a convenção "membro desconhecido" do DW —
# evita FK nula que quebraria análises e ferramentas de BI
_SK_DESCONHECIDO = 0


def build_fato_compras(
    df_compras: pl.DataFrame,
    dim_projeto: pl.DataFrame,
    dim_fornecedor: pl.DataFrame,
    dim_material: pl.DataFrame,
    dim_solicitacao: pl.DataFrame,
    dim_tempo: pl.DataFrame,
) -> pl.DataFrame:
    """
    Fato de compras — une todas as dimensões via surrogate keys.
    Métricas: valor_total_pedido, valor_alocado_projeto,
              quantidade_solicitada, qtd_pedidos.
    SKs nulas após o join são substituídas por 0 (membro desconhecido).
    """
    return (
        df_compras
        .join(dim_projeto,     on="id_projeto",     how="left")
        .join(dim_fornecedor,  on="id_fornecedor",  how="left")
        .join(dim_material,    on="id_material",    how="left")
        .join(dim_solicitacao, on="id_solicitacao", how="left")
        .join(dim_tempo,       left_on="data", right_on="data_completa", how="left")
        .select([
            "sk_projeto",
            "sk_fornecedor",
            "sk_material",
            "sk_solicitacao",
            "sk_tempo",
            "valor_total_pedido",
            "valor_alocado_projeto",
            "quantidade_solicitada",
            "qtd_pedidos",
        ])
        .with_columns([
            pl.col("sk_projeto").fill_null(_SK_DESCONHECIDO),
            pl.col("sk_fornecedor").fill_null(_SK_DESCONHECIDO),
            pl.col("sk_material").fill_null(_SK_DESCONHECIDO),
            pl.col("sk_solicitacao").fill_null(_SK_DESCONHECIDO),
            pl.col("sk_tempo").fill_null(_SK_DESCONHECIDO),
        ])
        .with_row_index("sk_fato")
    )


def build_fato_execucao_tarefas(
    df_execucao: pl.DataFrame,
    dim_projeto: pl.DataFrame,
    dim_tarefa: pl.DataFrame,
    dim_responsavel: pl.DataFrame,
    dim_tempo: pl.DataFrame,
) -> pl.DataFrame:
    """
    Fato de execução de tarefas.
    Métricas: horas_trabalhadas, horas_estimadas, qtd_registros.
    SKs nulas após o join são substituídas por 0 (membro desconhecido).
    """
    return (
        df_execucao
        .join(dim_projeto,     on="id_projeto",      how="left")
        .join(dim_tarefa,      on="id_tarefa",        how="left")
        .join(dim_responsavel, on="nome_responsavel", how="left")
        .join(dim_tempo,       left_on="data", right_on="data_completa", how="left")
        .select([
            "sk_projeto",
            "sk_tarefa",
            "sk_responsavel",
            "sk_tempo",
            "horas_trabalhadas",
            "horas_estimadas",
            "qtd_registros",
        ])
        .with_columns([
            pl.col("sk_projeto").fill_null(_SK_DESCONHECIDO),
            pl.col("sk_tarefa").fill_null(_SK_DESCONHECIDO),
            pl.col("sk_responsavel").fill_null(_SK_DESCONHECIDO),
            pl.col("sk_tempo").fill_null(_SK_DESCONHECIDO),
        ])
        .with_row_index("sk_fato")
    )


def build_fato_estoque_materiais(
    df_estoque: pl.DataFrame,
    dim_projeto: pl.DataFrame,
    dim_material: pl.DataFrame,
    dim_tempo: pl.DataFrame,
) -> pl.DataFrame:
    """
    Fato de estoque de materiais.
    Sem FK de fornecedor — correto conforme diagrama.
    Métricas: quantidade_estoque, quantidade_empenhada, custo_estimado_total.
    SKs nulas após o join são substituídas por 0 (membro desconhecido).
    """
    return (
        df_estoque
        .join(dim_projeto,  on="id_projeto",  how="left")
        .join(dim_material, on="id_material", how="left")
        .join(dim_tempo,    left_on="data", right_on="data_completa", how="left")
        .select([
            "sk_projeto",
            "sk_material",
            "sk_tempo",
            "quantidade_estoque",
            "quantidade_empenhada",
            "custo_estimado_total",
        ])
        .with_columns([
            pl.col("sk_projeto").fill_null(_SK_DESCONHECIDO),
            pl.col("sk_material").fill_null(_SK_DESCONHECIDO),
            pl.col("sk_tempo").fill_null(_SK_DESCONHECIDO),
        ])
        .with_row_index("sk_fato")
    )
