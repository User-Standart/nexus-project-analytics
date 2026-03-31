import polars as pl

_SK_DESCONHECIDO = 0


def _dim_lookup(dim: pl.DataFrame, sk_col: str, join_col: str) -> pl.DataFrame:
    """Retorna só as colunas necessárias da dimensão para o join."""
    return dim.select([sk_col, join_col])


def build_fato_compras(
    df_compras: pl.DataFrame,
    dim_projeto: pl.DataFrame,
    dim_fornecedor: pl.DataFrame,
    dim_material: pl.DataFrame,
    dim_solicitacao: pl.DataFrame,
    dim_tempo: pl.DataFrame,
) -> pl.DataFrame:
    return (
        df_compras
        .join(_dim_lookup(dim_projeto, "sk_projeto", "id_projeto"),
              on="id_projeto", how="left")
        .join(_dim_lookup(dim_fornecedor, "sk_fornecedor", "id_fornecedor"),
              on="id_fornecedor", how="left")
        .join(_dim_lookup(dim_material, "sk_material", "id_material"),
              on="id_material", how="left")
        .join(_dim_lookup(dim_solicitacao, "sk_solicitacao", "id_solicitacao"),
              on="id_solicitacao", how="left")
        .with_columns(pl.col("data").cast(pl.String).str.strptime(pl.Date, "%Y-%m-%d").alias("data_date"))
        .join(dim_tempo.select(["sk_tempo", "data_completa"]),
              left_on="data_date", right_on="data_completa", how="left")
        .select([
            "sk_projeto", "sk_fornecedor", "sk_material",
            "sk_solicitacao", "sk_tempo",
            "valor_total_pedido", "valor_alocado_projeto",
            "quantidade_solicitada", "qtd_pedidos",
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
    return (
        df_execucao
        .join(_dim_lookup(dim_projeto, "sk_projeto", "id_projeto"),
              on="id_projeto", how="left")
        .join(_dim_lookup(dim_tarefa, "sk_tarefa", "id_tarefa"),
              on="id_tarefa", how="left")
        .join(_dim_lookup(dim_responsavel, "sk_responsavel", "nome_responsavel"),
              on="nome_responsavel", how="left")
        .with_columns(pl.col("data").cast(pl.String).str.strptime(pl.Date, "%Y-%m-%d").alias("data_date"))
        .join(dim_tempo.select(["sk_tempo", "data_completa"]),
              left_on="data_date", right_on="data_completa", how="left")
        .select([
            "sk_projeto", "sk_tarefa", "sk_responsavel", "sk_tempo",
            "horas_trabalhadas", "horas_estimadas", "qtd_registros",
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
    return (
        df_estoque
        .join(_dim_lookup(dim_projeto, "sk_projeto", "id_projeto"),
              on="id_projeto", how="left")
        .join(_dim_lookup(dim_material, "sk_material", "id_material"),
              on="id_material", how="left")
        .with_columns(pl.col("data").cast(pl.String).str.strptime(pl.Date, "%Y-%m-%d").alias("data_date"))
        .join(dim_tempo.select(["sk_tempo", "data_completa"]),
              left_on="data_date", right_on="data_completa", how="left")
        .select([
            "sk_projeto", "sk_material", "sk_tempo",
            "quantidade_estoque", "quantidade_empenhada",
            "custo_estimado_total",
        ])
        .with_columns([
            pl.col("sk_projeto").fill_null(_SK_DESCONHECIDO),
            pl.col("sk_material").fill_null(_SK_DESCONHECIDO),
            pl.col("sk_tempo").fill_null(_SK_DESCONHECIDO),
        ])
        .with_row_index("sk_fato")
    )
