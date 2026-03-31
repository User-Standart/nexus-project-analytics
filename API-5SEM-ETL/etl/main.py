"""
main.py — ponto de entrada do pipeline ETL
Executa na ordem correta: Extract → Transform (dims) → Transform (fatos) → Load
"""
import polars as pl

from extract import extrair_fontes
from transform import (
    build_dim_tempo,
    build_dim_projeto,
    build_dim_fornecedor,
    build_dim_material,
    build_dim_responsavel,
    build_dim_tarefa,
    build_dim_solicitacao,
    build_fato_compras,
    build_fato_execucao_tarefas,
    build_fato_estoque_materiais,
)
from load import carregar_dw
from load_db import carregar_dw_postgres


def main():
    print("=== ETL — Star Schema ===\n")

    # ── 1. EXTRACT ────────────────────────────
    print("[1/3] Extraindo fontes...")
    fontes = extrair_fontes(pasta="data")  # aponte para a pasta dos CSVs

    # ── 2. TRANSFORM — dimensões ──────────────
    print("[2/3] Transformando dimensões...")

    # dim_tempo unifica datas de todas as fontes que a referenciam
    df_datas_unificadas = pl.concat([
        fontes["compras"].select("data"),
        fontes["execucao"].select("data"),
        fontes["estoque"].select("data"),
    ])
    dim_tempo        = build_dim_tempo(df_datas_unificadas)
    dim_projeto      = build_dim_projeto(fontes["projetos"])
    dim_fornecedor   = build_dim_fornecedor(fontes["fornecedores"])
    dim_material     = build_dim_material(fontes["materiais"])
    dim_responsavel  = build_dim_responsavel(fontes["execucao"])
    dim_tarefa       = build_dim_tarefa(fontes["tarefas"])
    dim_solicitacao  = build_dim_solicitacao(fontes["solicitacoes"])

    # ── 3. TRANSFORM — fatos ──────────────────
    print("[3/4] Transformando fatos...")
    fato_compras  = build_fato_compras(
        fontes["compras"],
        dim_projeto, dim_fornecedor,
        dim_material, dim_solicitacao, dim_tempo,
    )
    fato_execucao = build_fato_execucao_tarefas(
        fontes["execucao"],
        dim_projeto, dim_tarefa, dim_responsavel, dim_tempo,
    )
    fato_estoque  = build_fato_estoque_materiais(
        fontes["estoque"],
        dim_projeto, dim_material, dim_tempo,
    )

    # ── 4. LOAD ───────────────────────────────
    dimensoes = {
        "dim_tempo":       dim_tempo,
        "dim_projeto":     dim_projeto,
        "dim_fornecedor":  dim_fornecedor,
        "dim_material":    dim_material,
        "dim_responsavel": dim_responsavel,
        "dim_tarefa":      dim_tarefa,
        "dim_solicitacao": dim_solicitacao,
    }
    fatos = {
        "fato_compras":            fato_compras,
        "fato_execucao_tarefas":   fato_execucao,
        "fato_estoque_materiais":  fato_estoque,
    }

    print("[4/5] Carregando CSVs no DW...")
    carregar_dw(dimensoes=dimensoes, fatos=fatos, pasta_saida="dw")

    print("[5/5] Carregando no PostgreSQL...")
    carregar_dw_postgres(dimensoes=dimensoes, fatos=fatos)

    print("\n=== ETL concluído ===")


if __name__ == "__main__":
    main()
