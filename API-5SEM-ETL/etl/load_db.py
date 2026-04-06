import io
import os

import polars as pl
import psycopg

_DDL = """
CREATE SCHEMA IF NOT EXISTS dw;

DROP TABLE IF EXISTS dw.fato_compras           CASCADE;
DROP TABLE IF EXISTS dw.fato_execucao_tarefas  CASCADE;
DROP TABLE IF EXISTS dw.fato_estoque_materiais CASCADE;
DROP TABLE IF EXISTS dw.dim_solicitacao        CASCADE;
DROP TABLE IF EXISTS dw.dim_tarefa             CASCADE;
DROP TABLE IF EXISTS dw.dim_responsavel        CASCADE;
DROP TABLE IF EXISTS dw.dim_material           CASCADE;
DROP TABLE IF EXISTS dw.dim_fornecedor         CASCADE;
DROP TABLE IF EXISTS dw.dim_projeto            CASCADE;
DROP TABLE IF EXISTS dw.dim_tempo              CASCADE;

-- ── DIMENSÕES ────────────────────────────────

CREATE TABLE dw.dim_tempo (
    sk_tempo       INT PRIMARY KEY,
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

CREATE TABLE dw.dim_projeto (
    sk_projeto       INT PRIMARY KEY,
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

CREATE TABLE dw.dim_fornecedor (
    sk_fornecedor     INT PRIMARY KEY,
    id_fornecedor     INT,
    codigo_fornecedor VARCHAR(50),
    razao_social      VARCHAR(200),
    cidade            VARCHAR(100),
    estado            CHAR(2),
    categoria         VARCHAR(100),
    status            VARCHAR(50)
);

CREATE TABLE dw.dim_material (
    sk_material      INT PRIMARY KEY,
    id_material      INT,
    codigo_material  VARCHAR(50),
    descricao        VARCHAR(200),
    categoria        VARCHAR(100),
    fabricante       VARCHAR(100),
    custo_estimado   DECIMAL(10,2),
    status           VARCHAR(50)
);

CREATE TABLE dw.dim_responsavel (
    sk_responsavel    INT PRIMARY KEY,
    nome_responsavel  VARCHAR(100),
    tipo              VARCHAR(30)
);

CREATE TABLE dw.dim_tarefa (
    sk_tarefa        INT PRIMARY KEY,
    id_tarefa        INT,
    codigo_tarefa    VARCHAR(50),
    titulo           VARCHAR(200),
    status           VARCHAR(50),
    estimativa_horas INT,
    data_inicio      DATE,
    data_fim_prev    DATE
);

CREATE TABLE dw.dim_solicitacao (
    sk_solicitacao        INT PRIMARY KEY,
    id_solicitacao        INT,
    numero_solicitacao    VARCHAR(50),
    prioridade            VARCHAR(50),
    status_solicitacao    VARCHAR(50),
    numero_pedido         VARCHAR(50),
    status_pedido         VARCHAR(50),
    data_previsao_entrega DATE
);

-- ── FATOS ────────────────────────────────────

CREATE TABLE dw.fato_compras (
    sk_fato                INT PRIMARY KEY,
    sk_projeto             INT REFERENCES dw.dim_projeto(sk_projeto),
    sk_fornecedor          INT REFERENCES dw.dim_fornecedor(sk_fornecedor),
    sk_material            INT REFERENCES dw.dim_material(sk_material),
    sk_solicitacao         INT REFERENCES dw.dim_solicitacao(sk_solicitacao),
    sk_tempo               INT REFERENCES dw.dim_tempo(sk_tempo),
    valor_total_pedido     DECIMAL(12,2),
    valor_alocado_projeto  DECIMAL(12,2),
    quantidade_solicitada  INT,
    qtd_pedidos            INT
);

CREATE TABLE dw.fato_execucao_tarefas (
    sk_fato            INT PRIMARY KEY,
    sk_projeto         INT REFERENCES dw.dim_projeto(sk_projeto),
    sk_tarefa          INT REFERENCES dw.dim_tarefa(sk_tarefa),
    sk_responsavel     INT REFERENCES dw.dim_responsavel(sk_responsavel),
    sk_tempo           INT REFERENCES dw.dim_tempo(sk_tempo),
    horas_trabalhadas  DECIMAL(5,2),
    horas_estimadas    DECIMAL(5,2),
    qtd_registros      INT
);

CREATE TABLE dw.fato_estoque_materiais (
    sk_fato                INT PRIMARY KEY,
    sk_projeto             INT REFERENCES dw.dim_projeto(sk_projeto),
    sk_material            INT REFERENCES dw.dim_material(sk_material),
    sk_tempo               INT REFERENCES dw.dim_tempo(sk_tempo),
    quantidade_estoque     INT,
    quantidade_empenhada   INT,
    custo_estimado_total   DECIMAL(12,2)
);
"""


def _copy_df(cur, table: str, df: pl.DataFrame) -> None:
    """Carrega um DataFrame no PostgreSQL usando COPY (rápido)."""
    buf = io.StringIO()
    df.write_csv(buf)
    buf.seek(0)
    cols = ", ".join(df.columns)
    with cur.copy(f"COPY {table} ({cols}) FROM STDIN WITH CSV HEADER") as copy:
        while chunk := buf.read(8192):
            copy.write(chunk)


def carregar_dw_postgres(
    dimensoes: dict[str, pl.DataFrame],
    fatos: dict[str, pl.DataFrame],
) -> None:
    """Cria o schema dw e carrega dimensões e fatos no PostgreSQL."""
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        print("  [db] DATABASE_URL não definida, pulando carga no banco.")
        return

    with psycopg.connect(database_url) as conn:
        with conn.cursor() as cur:
            print("  [db] Criando schema e tabelas...")
            cur.execute(_DDL)

            ordem_dims = [
                "dim_tempo",
                "dim_projeto",
                "dim_fornecedor",
                "dim_material",
                "dim_responsavel",
                "dim_tarefa",
                "dim_solicitacao",
            ]
            for nome in ordem_dims:
                _copy_df(cur, f"dw.{nome}", dimensoes[nome])
                print(f"  [db] {nome}: {len(dimensoes[nome])} linhas")

            for nome, df in fatos.items():
                _copy_df(cur, f"dw.{nome}", df)
                print(f"  [db] {nome}: {len(df)} linhas")

        conn.commit()
        print("  [db] Carga concluída com sucesso.")
