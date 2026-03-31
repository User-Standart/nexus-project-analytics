import polars as pl


def extrair_fontes(pasta: str = "data") -> dict[str, pl.DataFrame]:
    """
    Lê os CSVs OLTP e retorna DataFrames brutos com colunas renomeadas
    para o padrão id_<entidade> e <entidade>_id → id_<entidade>.
    """
    programas = (
        pl.read_csv(f"{pasta}/programas.csv")
        .rename({"id": "id_programa"})
    )
    projetos = (
        pl.read_csv(f"{pasta}/projetos.csv")
        .rename({"id": "id_projeto", "programa_id": "id_programa"})
    )
    tarefas = (
        pl.read_csv(f"{pasta}/tarefas_projeto.csv")
        .rename({
            "id": "id_tarefa",
            "projeto_id": "id_projeto",
            "data_fim_prevista": "data_fim_prev",
        })
    )
    tempo_tarefas = (
        pl.read_csv(f"{pasta}/tempo_tarefas.csv")
        .rename({"id": "id_tempo", "tarefa_id": "id_tarefa"})
    )
    materiais = (
        pl.read_csv(f"{pasta}/materiais.csv")
        .rename({"id": "id_material"})
    )
    fornecedores = (
        pl.read_csv(f"{pasta}/fornecedores.csv")
        .rename({"id": "id_fornecedor"})
    )
    solicitacoes = (
        pl.read_csv(f"{pasta}/solicitacoes_compra.csv")
        .rename({
            "id": "id_solicitacao",
            "projeto_id": "id_projeto",
            "material_id": "id_material",
        })
    )
    pedidos = (
        pl.read_csv(f"{pasta}/pedidos_compra.csv")
        .rename({
            "id": "id_pedido",
            "solicitacao_id": "id_solicitacao",
            "fornecedor_id": "id_fornecedor",
        })
    )
    compras_projeto = (
        pl.read_csv(f"{pasta}/compras_projeto.csv")
        .rename({
            "id": "id_compra_projeto",
            "pedido_compra_id": "id_pedido",
            "projeto_id": "id_projeto",
        })
    )
    empenho = (
        pl.read_csv(f"{pasta}/empenho_materiais.csv")
        .rename({
            "id": "id_empenho",
            "projeto_id": "id_projeto",
            "material_id": "id_material",
        })
    )
    estoque = (
        pl.read_csv(f"{pasta}/estoque_materiais_projeto.csv")
        .rename({
            "id": "id_estoque",
            "projeto_id": "id_projeto",
            "material_id": "id_material",
        })
    )

    return {
        "programas":       programas,
        "projetos":        projetos,
        "tarefas":         tarefas,
        "tempo_tarefas":   tempo_tarefas,
        "materiais":       materiais,
        "fornecedores":    fornecedores,
        "solicitacoes":    solicitacoes,
        "pedidos":         pedidos,
        "compras_projeto": compras_projeto,
        "empenho":         empenho,
        "estoque":         estoque,
    }


def denormalizar(fontes: dict[str, pl.DataFrame]) -> dict[str, pl.DataFrame]:
    """
    Junta as tabelas OLTP normalizadas em visões denormalizadas
    que o transform do star schema espera.
    """

    # ── projetos + programas ──
    projetos_dn = (
        fontes["projetos"]
        .join(fontes["programas"], on="id_programa", how="left", suffix="_prog")
        .select([
            "id_projeto", "codigo_projeto", "nome_projeto",
            "responsavel", "status",
            "codigo_programa", "nome_programa", "gerente_programa",
            "data_inicio", "data_fim_prevista",
        ])
    )

    # ── solicitacoes + pedidos (para dim_solicitacao) ──
    solicitacoes_dn = (
        fontes["solicitacoes"]
        .join(fontes["pedidos"], on="id_solicitacao", how="left", suffix="_ped")
        .select([
            "id_solicitacao", "numero_solicitacao",
            "prioridade",
            pl.col("status").alias("status_solicitacao"),
            "numero_pedido",
            pl.col("status_ped").alias("status_pedido"),
            "data_previsao_entrega",
        ])
    )

    # ── execucao: tempo_tarefas + tarefas ──
    execucao_dn = (
        fontes["tempo_tarefas"]
        .join(fontes["tarefas"], on="id_tarefa", how="left", suffix="_tar")
        .select([
            "id_projeto",
            "id_tarefa",
            pl.col("usuario").alias("nome_responsavel"),
            "data",
            "horas_trabalhadas",
            pl.col("estimativa_horas").cast(pl.Decimal(5, 2)).alias("horas_estimadas"),
            pl.lit(1).alias("qtd_registros"),
        ])
    )

    # ── compras: compras_projeto + pedidos + solicitacoes ──
    compras_dn = (
        fontes["compras_projeto"]
        .join(fontes["pedidos"], on="id_pedido", how="left", suffix="_ped")
        .join(fontes["solicitacoes"], on="id_solicitacao", how="left", suffix="_sol")
        .select([
            "id_projeto",
            "id_fornecedor",
            "id_material",
            "id_solicitacao",
            pl.col("data_pedido").alias("data"),
            pl.col("valor_total").alias("valor_total_pedido"),
            pl.col("valor_alocado").alias("valor_alocado_projeto"),
            pl.col("quantidade").alias("quantidade_solicitada"),
            pl.lit(1).alias("qtd_pedidos"),
        ])
    )

    # ── estoque: estoque + empenho + materiais ──
    estoque_dn = (
        fontes["estoque"]
        .join(
            fontes["empenho"],
            on=["id_projeto", "id_material"],
            how="left",
            suffix="_emp",
        )
        .join(fontes["materiais"], on="id_material", how="left", suffix="_mat")
        .select([
            "id_projeto",
            "id_material",
            pl.col("data_empenho").alias("data"),
            pl.col("quantidade").alias("quantidade_estoque"),
            pl.col("quantidade_empenhada").fill_null(0),
            (pl.col("custo_estimado") * pl.col("quantidade")).alias("custo_estimado_total"),
        ])
    )

    return {
        "projetos":     projetos_dn,
        "fornecedores": fontes["fornecedores"],
        "materiais":    fontes["materiais"],
        "solicitacoes": solicitacoes_dn,
        "tarefas":      fontes["tarefas"],
        "execucao":     execucao_dn,
        "compras":      compras_dn,
        "estoque":      estoque_dn,
    }
