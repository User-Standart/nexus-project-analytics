import polars as pl


def build_dim_tempo(df_datas: pl.DataFrame) -> pl.DataFrame:
    """
    Gera a dim_tempo a partir de um DataFrame com coluna 'data'.
    Deve receber o concat de TODAS as fontes que usam tempo
    (compras, execucao, estoque) para cobrir todas as datas do DW.
    Inclui: ano, semestre, trimestre, mes, nome_mes, semana, dia, dia_semana.
    """
    # lookup vetorial de mes → nome: substitui map_elements, muito mais rápido
    lookup_mes = pl.DataFrame({
        "mes_num": list(range(1, 13)),
        "nome_mes": [
            "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
            "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro",
        ],
    }).with_columns(pl.col("mes_num").cast(pl.Int32))

    df = (
        df_datas
        .select([pl.col("data").alias("data_completa")])
        .unique()
        .with_columns([
            pl.col("data_completa").str.strptime(pl.Date, "%Y-%m-%d"),
            pl.col("data_completa").dt.year().alias("ano"),
            pl.col("data_completa").dt.month().cast(pl.Int32).alias("mes"),
            pl.col("data_completa").dt.day().alias("dia"),
            pl.col("data_completa").dt.weekday().alias("dia_semana"),
            pl.col("data_completa").dt.week().alias("semana"),
        ])
        .with_columns([
            pl.when(pl.col("mes") <= 6).then(1).otherwise(2).alias("semestre"),
            pl.when(pl.col("mes") <= 3).then(1)
              .when(pl.col("mes") <= 6).then(2)
              .when(pl.col("mes") <= 9).then(3)
              .otherwise(4).alias("trimestre"),
        ])
        # join vetorial substitui map_elements — ordens de grandeza mais rápido
        .join(lookup_mes, left_on="mes", right_on="mes_num", how="left")
        .with_row_index("sk_tempo")
    )
    return df


def build_dim_projeto(df_projetos: pl.DataFrame) -> pl.DataFrame:
    return (
        df_projetos
        .select([
            "id_projeto", "codigo_projeto", "nome_projeto",
            "responsavel", "status", "codigo_programa",
            "nome_programa", "gerente_programa",
            "data_inicio", "data_fim_prevista",
        ])
        .unique()
        .with_row_index("sk_projeto")
    )


def build_dim_fornecedor(df_fornecedores: pl.DataFrame) -> pl.DataFrame:
    return (
        df_fornecedores
        .select([
            "id_fornecedor", "codigo_fornecedor", "razao_social",
            "cidade", "estado", "categoria", "status",
        ])
        .unique()
        .with_row_index("sk_fornecedor")
    )


def build_dim_material(df_materiais: pl.DataFrame) -> pl.DataFrame:
    return (
        df_materiais
        .select([
            "id_material", "codigo_material", "descricao",
            "categoria", "fabricante", "custo_estimado", "status",
        ])
        .unique()
        .with_row_index("sk_material")
    )


def build_dim_responsavel(df_execucao: pl.DataFrame) -> pl.DataFrame:
    """
    Extrai responsáveis únicos do CSV de execução.
    Se a coluna 'tipo' não existir na fonte, preenche com 'Indefinido'.
    """
    if "tipo" not in df_execucao.columns:
        df_execucao = df_execucao.with_columns(
            pl.lit("Indefinido").alias("tipo")
        )
    return (
        df_execucao
        .select(["nome_responsavel", "tipo"])
        .unique()
        .with_row_index("sk_responsavel")
    )


def build_dim_tarefa(df_tarefas: pl.DataFrame) -> pl.DataFrame:
    return (
        df_tarefas
        .select([
            "id_tarefa", "codigo_tarefa", "titulo",
            "status", "estimativa_horas",
            "data_inicio", "data_fim_prev",
        ])
        .unique()
        .with_row_index("sk_tarefa")
    )


def build_dim_solicitacao(df_solicitacoes: pl.DataFrame) -> pl.DataFrame:
    return (
        df_solicitacoes
        .select([
            "id_solicitacao", "numero_solicitacao", "prioridade",
            "status_solicitacao", "numero_pedido",
            "status_pedido", "data_previsao_entrega",
        ])
        .unique()
        .with_row_index("sk_solicitacao")
    )
