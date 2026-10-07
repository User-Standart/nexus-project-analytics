import io
import os

import polars as pl
import psycopg

_DDL = """
CREATE SCHEMA IF NOT EXISTS dw;

CREATE TABLE IF NOT EXISTS dw.dim_tempo (
    sk_tempo       BIGINT PRIMARY KEY,
    data_completa  DATE,
    ano            INT,
    semestre       INT,
    trimestre      INT,
    mes            INT,
    nome_mes       VARCHAR(50),
    semana         INT,
    dia            INT,
    dia_semana     VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS dw.dim_projeto (
    sk_projeto       BIGINT PRIMARY KEY,
    id_projeto       INT,
    codigo_projeto   VARCHAR(50),
    nome_projeto     VARCHAR(100),
    responsavel      VARCHAR(100),
    status           VARCHAR(50),
    codigo_programa  VARCHAR(50),
    nome_programa    VARCHAR(100),
    gerente_programa VARCHAR(100),
    data_inicio      DATE,
    data_fim_prevista DATE
);

CREATE TABLE IF NOT EXISTS dw.dim_fornecedor (
    sk_fornecedor     BIGINT PRIMARY KEY,
    id_fornecedor     INT,
    codigo_fornecedor VARCHAR(50),
    razao_social      VARCHAR(200),
    cidade            VARCHAR(100),
    estado            CHAR(2),
    categoria         VARCHAR(100),
    status            VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS dw.dim_material (
    sk_material      BIGINT PRIMARY KEY,
    id_material      INT,
    codigo_material  VARCHAR(50),
    descricao        VARCHAR(200),
    categoria        VARCHAR(100),
    fabricante       VARCHAR(100),
    custo_estimado   DECIMAL(10,2),
    status           VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS dw.dim_responsavel (
    sk_responsavel    BIGINT PRIMARY KEY,
    nome_responsavel  VARCHAR(100),
    tipo              VARCHAR(30)
);

CREATE TABLE IF NOT EXISTS dw.dim_tarefa (
    sk_tarefa        BIGINT PRIMARY KEY,
    id_tarefa        INT,
    codigo_tarefa    VARCHAR(50),
    titulo           VARCHAR(200),
    status           VARCHAR(50),
    estimativa_horas INT,
    data_inicio      DATE,
    data_fim_prev    DATE
);

CREATE TABLE IF NOT EXISTS dw.dim_solicitacao (
    sk_solicitacao        BIGINT PRIMARY KEY,
    id_solicitacao        INT,
    numero_solicitacao    VARCHAR(50),
    prioridade            VARCHAR(50),
    status_solicitacao    VARCHAR(50),
    numero_pedido         VARCHAR(50),
    status_pedido         VARCHAR(50),
    data_previsao_entrega DATE
);

CREATE TABLE IF NOT EXISTS dw.fato_compras (
    sk_fato                BIGINT PRIMARY KEY,
    sk_projeto             BIGINT REFERENCES dw.dim_projeto(sk_projeto),
    sk_fornecedor          BIGINT REFERENCES dw.dim_fornecedor(sk_fornecedor),
    sk_material            BIGINT REFERENCES dw.dim_material(sk_material),
    sk_solicitacao         BIGINT REFERENCES dw.dim_solicitacao(sk_solicitacao),
    sk_tempo               BIGINT REFERENCES dw.dim_tempo(sk_tempo),
    valor_total_pedido     DECIMAL(12,2),
    valor_alocado_projeto  DECIMAL(12,2),
    quantidade_solicitada  INT,
    qtd_pedidos            INT
);

CREATE TABLE IF NOT EXISTS dw.fato_execucao_tarefas (
    sk_fato            BIGINT PRIMARY KEY,
    sk_projeto         BIGINT REFERENCES dw.dim_projeto(sk_projeto),
    sk_tarefa          BIGINT REFERENCES dw.dim_tarefa(sk_tarefa),
    sk_responsavel     BIGINT REFERENCES dw.dim_responsavel(sk_responsavel),
    sk_tempo           BIGINT REFERENCES dw.dim_tempo(sk_tempo),
    horas_trabalhadas  DECIMAL(5,2),
    horas_estimadas    DECIMAL(5,2),
    qtd_registros      INT
);

CREATE TABLE IF NOT EXISTS dw.fato_estoque_materiais (
    sk_fato                BIGINT PRIMARY KEY,
    sk_projeto             BIGINT REFERENCES dw.dim_projeto(sk_projeto),
    sk_material            BIGINT REFERENCES dw.dim_material(sk_material),
    sk_tempo               BIGINT REFERENCES dw.dim_tempo(sk_tempo),
    quantidade_estoque     INT,
    quantidade_empenhada   INT,
    custo_estimado_total   DECIMAL(12,2)
);
"""


def _upsert_df(cur, table: str, df: pl.DataFrame, pk: str) -> int:
    if df.is_empty():
        return 0

    buf = io.StringIO()
    df.write_csv(buf)
    buf.seek(0)

    tmp = f"_tmp_{table.replace('.', '_')}"
    cols = ", ".join(df.columns)
    col_defs = ", ".join(f"{c} TEXT" for c in df.columns)

    cur.execute(f"CREATE TEMP TABLE {tmp} ({col_defs}) ON COMMIT DROP")

    with cur.copy(f"COPY {tmp} ({cols}) FROM STDIN WITH CSV HEADER") as copy:
        while chunk := buf.read(8192):
            copy.write(chunk)

    select_cols = ", ".join(
        (
            f"{c}::BIGINT"
            if c == pk or c.startswith("sk_") or c.startswith("id_")

            else f"{c}::DECIMAL"
            if (
                "valor" in c.lower()
                or "custo" in c.lower()
                or "horas" in c.lower()
            )

            else f"{c}::DATE"
            if "data" in c.lower()

            else f"{c}::INT"
            if c in {
                "ano",
                "semestre",
                "trimestre",
                "mes",
                "semana",
                "dia",
                "qtd_pedidos",
                "qtd_registros",
                "quantidade_solicitada",
                "quantidade_estoque",
                "quantidade_empenhada",
            }

            else c
        )
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

def carregar_dw_postgres(
    dimensoes: dict[str, pl.DataFrame],
    fatos: dict[str, pl.DataFrame],
) -> None:
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        return

    with psycopg.connect(database_url) as conn:
        with conn.cursor() as cur:
            print("  [db] Garantindo tabelas do DW...")
            cur.execute(_DDL)

            ordem_dims = [
                "dim_tempo", "dim_projeto", "dim_fornecedor",
                "dim_material", "dim_responsavel", "dim_tarefa", "dim_solicitacao",
            ]
            
            for nome in ordem_dims:
                pk = "sk_" + nome.replace("dim_", "")
                count = _upsert_df(cur, f"dw.{nome}", dimensoes[nome], pk)
                print(f"  [db] {nome}: {count} processadas")

            for nome, df in fatos.items():
                count = _upsert_df(cur, f"dw.{nome}", df, "sk_fato")
                print(f"  [db] {nome}: {count} processadas")

        conn.commit()
