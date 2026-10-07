import io
import os

import polars as pl
import psycopg

_TABLE_MAP = [
    ("programas", "programa", {
        "id_programa": "id_programa",
        "codigo_programa": "codigo_programa",
        "nome_programa": "nome_programa",
        "gerente_programa": "gerente_programa",
        "gerente_tecnico": "gerente_tecnico",
        "data_inicio": "data_inicio",
        "data_fim_prevista": "data_fim_prevista",
        "status": "status",
    }),
    ("projetos", "projeto", {
        "id_projeto": "id_projeto",
        "codigo_projeto": "codigo_projeto",
        "nome_projeto": "nome_projeto",
        "id_programa": "id_programa",
        "responsavel": "responsavel",
        "custo_hora": "custo_hora",
        "data_inicio": "data_inicio",
        "data_fim_prevista": "data_fim_prevista",
        "status": "status",
    }),
    ("tarefas", "tarefa", {
        "id_tarefa": "id_tarefa",
        "codigo_tarefa": "codigo_tarefa",
        "id_projeto": "id_projeto",
        "titulo": "titulo",
        "responsavel": "responsavel",
        "estimativa_horas": "estimativa_horas",
        "data_inicio": "data_inicio",
        "data_fim_prev": "data_fim_prevista",
        "status": "status",
    }),
    ("tempo_tarefas", "tempo_tarefa", {
        "id_tempo": "id_tempo",
        "id_tarefa": "id_tarefa",
        "usuario": "usuario",
        "data": "data",
        "horas_trabalhadas": "horas_trabalhadas",
    }),
    ("materiais", "material", {
        "id_material": "id_material",
        "codigo_material": "codigo_material",
        "descricao": "descricao",
        "categoria": "categoria",
        "fabricante": "fabricante",
        "custo_estimado": "custo_estimado",
        "status": "status",
    }),
    ("fornecedores", "fornecedor", {
        "id_fornecedor": "id_fornecedor",
        "codigo_fornecedor": "codigo_fornecedor",
        "razao_social": "razao_social",
        "cidade": "cidade",
        "estado": "estado",
        "categoria": "categoria",
        "status": "status",
    }),
    ("solicitacoes", "solicitacao_compra", {
        "id_solicitacao": "id_solicitacao",
        "numero_solicitacao": "numero_solicitacao",
        "id_projeto": "id_projeto",
        "id_material": "id_material",
        "quantidade": "quantidade",
        "data_solicitacao": "data_solicitacao",
        "prioridade": "prioridade",
        "status": "status",
    }),
    ("pedidos", "pedido_compra", {
        "id_pedido": "id_pedido",
        "numero_pedido": "numero_pedido",
        "id_solicitacao": "id_solicitacao",
        "id_fornecedor": "id_fornecedor",
        "data_pedido": "data_pedido",
        "data_previsao_entrega": "data_previsao_entrega",
        "valor_total": "valor_total",
        "status": "status",
    }),
    ("compras_projeto", "compra_projeto", {
        "id_compra_projeto": "id_compra_projeto",
        "id_pedido": "id_pedido",
        "id_projeto": "id_projeto",
        "valor_alocado": "valor_alocado",
    }),
    ("empenho", "empenho", {
        "id_empenho": "id_empenho",
        "id_projeto": "id_projeto",
        "id_material": "id_material",
        "quantidade_empenhada": "quantidade_empenhada",
        "data_empenho": "data_empenho",
    }),
    ("estoque", "estoque_projeto", {
        "id_estoque": "id_estoque",
        "id_projeto": "id_projeto",
        "id_material": "id_material",
        "quantidade": "quantidade",
        "localizacao": "localizacao",
    }),
]


def _upsert_df(cur, table: str, df: pl.DataFrame, pk: str) -> int:
    if df.is_empty():
        return 0

    buf = io.StringIO()
    df.write_csv(buf)
    buf.seek(0)

    tmp = f"_tmp_{table}"
    cols = ", ".join(df.columns)
    col_defs = ", ".join(f"{c} TEXT" for c in df.columns)

    cur.execute(f"CREATE TEMP TABLE {tmp} ({col_defs}) ON COMMIT DROP")

    with cur.copy(f"COPY {tmp} ({cols}) FROM STDIN WITH CSV HEADER") as copy:
        while chunk := buf.read(8192):
            copy.write(chunk)

    select_cols = ", ".join(
        f"{c}::INTEGER"
        if (
            c == pk
            or c.startswith("id_")
            or "quantidade" in c
            or "estimativa" in c
        )
        else f"{c}::DECIMAL"
        if (
            "valor" in c
            or "custo" in c
            or "horas" in c
        )
        else f"{c}::DATE"
        if "data" in c.lower()
        else c
        for c in df.columns
    )

    cur.execute(f"""
        INSERT INTO {table} ({cols})
        SELECT {select_cols}
        FROM {tmp}
        ON CONFLICT ({pk}) DO NOTHING
    """)

    cur.execute(f"SELECT COUNT(*) FROM {tmp}")
    row = cur.fetchone()

    return row[0] if row else 0


def carregar_oltp(fontes: dict[str, pl.DataFrame]) -> None:
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        return

    with psycopg.connect(database_url) as conn:
        with conn.cursor() as cur:
            for fonte_nome, table, col_map in _TABLE_MAP:
                df = fontes[fonte_nome]

                src_cols = list(col_map.keys())
                dst_cols = list(col_map.values())

                df_out = df.select(src_cols).rename(
                    {s: d for s, d in zip(src_cols, dst_cols) if s != d}
                )

                pk = dst_cols[0]

                print(f"\n=== {table} ===")
                print(df_out.schema)

                count = _upsert_df(cur, table, df_out, pk)
                print(f"  [oltp] {table}: {count} linhas novas/verificadas")

        conn.commit()
        