import glob
import polars as pl

# Colunas com constraint UNIQUE no banco que precisam de prefixo de versão
# para evitar conflito quando o mesmo código aparece em v1 e v2
_CODIGO_COLS: dict[str, list[str]] = {
    "programas.csv":           ["codigo_programa"],
    "projetos.csv":            ["codigo_projeto"],
    "tarefas_projeto.csv":     ["codigo_tarefa"],
    "materiais.csv":           ["codigo_material"],
    "fornecedores.csv":        ["codigo_fornecedor"],
    "solicitacoes_compra.csv": ["numero_solicitacao"],
    "pedidos_compra.csv":      ["numero_pedido"],
}

# Mapeamento: nome_arquivo -> coluna PK e colunas FK que referenciam outras tabelas
_SCHEMA: dict[str, dict] = {
    "programas.csv": {
        "pk": "id",
        "fks": {},
    },
    "projetos.csv": {
        "pk": "id",
        "fks": {"programa_id": "programas.csv"},
    },
    "tarefas_projeto.csv": {
        "pk": "id",
        "fks": {"projeto_id": "projetos.csv"},
    },
    "tempo_tarefas.csv": {
        "pk": "id",
        "fks": {"tarefa_id": "tarefas_projeto.csv"},
    },
    "materiais.csv": {
        "pk": "id",
        "fks": {},
    },
    "fornecedores.csv": {
        "pk": "id",
        "fks": {},
    },
    "solicitacoes_compra.csv": {
        "pk": "id",
        "fks": {
            "projeto_id": "projetos.csv",
            "material_id": "materiais.csv",
        },
    },
    "pedidos_compra.csv": {
        "pk": "id",
        "fks": {
            "solicitacao_id": "solicitacoes_compra.csv",
            "fornecedor_id": "fornecedores.csv",
        },
    },
    "compras_projeto.csv": {
        "pk": "id",
        "fks": {
            "pedido_compra_id": "pedidos_compra.csv",
            "projeto_id": "projetos.csv",
        },
    },
    "empenho_materiais.csv": {
        "pk": "id",
        "fks": {
            "projeto_id": "projetos.csv",
            "material_id": "materiais.csv",
        },
    },
    "estoque_materiais_projeto.csv": {
        "pk": "id",
        "fks": {
            "projeto_id": "projetos.csv",
            "material_id": "materiais.csv",
        },
    },
}


def _calcular_offsets(pasta: str) -> dict[str, int]:
    """
    Para cada tabela, decide se a v2 precisa de offset nos IDs.

    Há dois cenários possíveis quando um ID aparece em ambas as versões:

      1. Conteúdo IDÊNTICO → a v2 simplesmente já contém os registros
         da v1 (reutilização intencional). Basta fazer unique() depois
         de concat; offset = 0.

      2. Conteúdo DIFERENTE → o mesmo ID foi reutilizado para um
         registro completamente novo (bug na origem). Conforme
         orientação da PO: nunca substituir, sempre adicionar com
         novo ID. Nesse caso offset = max(id_v1), deslocando TODOS
         os IDs da v2 para evitar qualquer colisão.
    """
    offsets: dict[str, int] = {}

    for nome_arquivo, info in _SCHEMA.items():
        v1_paths = glob.glob(f"{pasta}/v1/{nome_arquivo}")
        v2_paths = glob.glob(f"{pasta}/v2/{nome_arquivo}")

        if not v1_paths or not v2_paths:
            offsets[nome_arquivo] = 0
            continue

        df_v1 = pl.read_csv(v1_paths[0])
        df_v2 = pl.read_csv(v2_paths[0])

        ids_comuns = set(df_v1[info["pk"]].to_list()) & set(df_v2[info["pk"]].to_list())

        if not ids_comuns:
            # Sem sobreposição alguma: sem necessidade de offset
            offsets[nome_arquivo] = 0
            continue

        # Compara o conteúdo dos registros com IDs em comum
        v1_comuns = df_v1.filter(pl.col(info["pk"]).is_in(list(ids_comuns))).sort(info["pk"])
        v2_comuns = df_v2.filter(pl.col(info["pk"]).is_in(list(ids_comuns))).sort(info["pk"])

        ha_conflito = any(
            r1 != r2
            for r1, r2 in zip(v1_comuns.to_dicts(), v2_comuns.to_dicts())
        )

        if ha_conflito:
            # IDs reutilizados com dados diferentes → desloca v2 inteira
            offsets[nome_arquivo] = int(df_v1[info["pk"]].max())
        else:
            # IDs em comum com dados idênticos → v2 já inclui v1, sem conflito
            offsets[nome_arquivo] = 0

    return offsets


def _aplicar_prefixo(df: pl.DataFrame, nome_arquivo: str, versao: str) -> pl.DataFrame:
    """
    Prefixa as colunas de código com 'v1-' ou 'v2-' para evitar conflito
    com a constraint UNIQUE do banco OLTP, que não admite o mesmo código
    em registros distintos mesmo que venham de versões diferentes.
    """
    cols = _CODIGO_COLS.get(nome_arquivo, [])
    for col in cols:
        if col in df.columns:
            df = df.with_columns(
                (pl.lit(f"{versao}-") + pl.col(col)).alias(col)
            )
    return df


def _aplicar_offset(df: pl.DataFrame, nome_arquivo: str, offset: int,
                    offsets: dict[str, int]) -> pl.DataFrame:
    """
    Aplica offset na PK do DataFrame e em cada FK cujo arquivo referenciado
    também possui offset > 0, preservando a integridade referencial interna da v2.
    """
    if offset == 0:
        return df

    info = _SCHEMA[nome_arquivo]
    pk = info["pk"]

    df = df.with_columns(pl.col(pk) + offset)

    for fk_col, ref_arquivo in info["fks"].items():
        ref_offset = offsets.get(ref_arquivo, 0)
        if ref_offset > 0 and fk_col in df.columns:
            df = df.with_columns(pl.col(fk_col) + ref_offset)

    return df


def ler_acumulado(pasta: str, nome_arquivo: str,
                  offsets: dict[str, int]) -> pl.DataFrame:
    """
    Lê v1 e v2 de forma acumulativa aplicando a estratégia correta por tabela:

    - offset = 0 (ex: projetos, programas): v2 já contém v1 com dados
      idênticos. Faz concat e deduplica por ID (unique keep='first'),
      resultando apenas nos registros únicos sem duplicação.

    - offset > 0 (ex: tarefas, materiais...): IDs foram reutilizados com
      dados diferentes. Desloca todos os IDs da v2 antes do concat,
      garantindo que cada registro de origem seja preservado como novo.

    Em ambos os casos, colunas de código com UNIQUE no banco recebem
    prefixo de versão ('v1-' / 'v2-') para evitar violação de constraint.
    """
    v1_paths = glob.glob(f"{pasta}/v1/{nome_arquivo}")
    v2_paths = glob.glob(f"{pasta}/v2/{nome_arquivo}")

    if not v1_paths and not v2_paths:
        raise FileNotFoundError(
            f"Nenhum arquivo '{nome_arquivo}' encontrado em '{pasta}/v1' ou '{pasta}/v2'."
        )

    dfs = []

    for path in sorted(v1_paths):
        df = pl.read_csv(path, try_parse_dates=True)
        df = _aplicar_prefixo(df, nome_arquivo, "v1")
        dfs.append(df)

    offset = offsets.get(nome_arquivo, 0)
    for path in sorted(v2_paths):
        df = pl.read_csv(path, try_parse_dates=True)
        df = _aplicar_prefixo(df, nome_arquivo, "v2")
        df = _aplicar_offset(df, nome_arquivo, offset, offsets)
        dfs.append(df)

    df_combined = pl.concat(dfs)

    # Se não há offset, a v2 já continha v1: remove duplicatas por PK
    if offset == 0:
        pk = _SCHEMA[nome_arquivo]["pk"]
        df_combined = df_combined.unique(subset=[pk], keep="first")

    # Garante conversão de colunas de data que ainda sejam String
    for col_name in df_combined.columns:
        if "data" in col_name.lower() and df_combined[col_name].dtype == pl.String:
            df_combined = df_combined.with_columns(
                pl.col(col_name).str.to_date(strict=False)
            )

    return df_combined


def extrair_fontes(pasta: str = "data") -> dict[str, pl.DataFrame]:
    """
    Lê todas as tabelas de forma acumulativa (v1 + v2).

    - Registros com IDs idênticos e conteúdo igual são deduplicados (sem duplicação).
    - Registros com IDs reutilizados mas conteúdo diferente recebem novo ID
      e são SEMPRE adicionados, nunca substituídos.
    """
    offsets = _calcular_offsets(pasta)

    programas = (
        ler_acumulado(pasta, "programas.csv", offsets)
        .rename({"id": "id_programa"})
    )

    projetos = (
        ler_acumulado(pasta, "projetos.csv", offsets)
        .rename({"id": "id_projeto", "programa_id": "id_programa"})
    )

    tarefas = (
        ler_acumulado(pasta, "tarefas_projeto.csv", offsets)
        .rename({
            "id": "id_tarefa",
            "projeto_id": "id_projeto",
            "data_fim_prevista": "data_fim_prev",
        })
    )

    tempo_tarefas = (
        ler_acumulado(pasta, "tempo_tarefas.csv", offsets)
        .rename({"id": "id_tempo", "tarefa_id": "id_tarefa"})
    )

    materiais = (
        ler_acumulado(pasta, "materiais.csv", offsets)
        .rename({"id": "id_material"})
    )

    fornecedores = (
        ler_acumulado(pasta, "fornecedores.csv", offsets)
        .rename({"id": "id_fornecedor"})
    )

    solicitacoes = (
        ler_acumulado(pasta, "solicitacoes_compra.csv", offsets)
        .rename({
            "id": "id_solicitacao",
            "projeto_id": "id_projeto",
            "material_id": "id_material",
        })
    )

    pedidos = (
        ler_acumulado(pasta, "pedidos_compra.csv", offsets)
        .rename({
            "id": "id_pedido",
            "solicitacao_id": "id_solicitacao",
            "fornecedor_id": "id_fornecedor",
        })
    )

    compras_projeto = (
        ler_acumulado(pasta, "compras_projeto.csv", offsets)
        .rename({
            "id": "id_compra_projeto",
            "pedido_compra_id": "id_pedido",
            "projeto_id": "id_projeto",
        })
    )

    empenho = (
        ler_acumulado(pasta, "empenho_materiais.csv", offsets)
        .rename({
            "id": "id_empenho",
            "projeto_id": "id_projeto",
            "material_id": "id_material",
        })
    )

    estoque = (
        ler_acumulado(pasta, "estoque_materiais_projeto.csv", offsets)
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
