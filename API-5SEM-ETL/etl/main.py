"""
main.py — ponto de entrada do pipeline ETL
Extract → Load OLTP → Transform (dims + fatos) → Load DW
"""
import polars as pl

from extract import extrair_fontes, denormalizar
from load import carregar_dw
from load_oltp import carregar_oltp
from load_db import carregar_dw_postgres
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


def main():
    print("=== ETL Pipeline ===\n")

    # ── 1. EXTRACT ────────────────────────────
    print("[1/6] Extraindo fontes CSV...")
    fontes = extrair_fontes(pasta="data")

    # ── 2. LOAD OLTP ─────────────────────────
    print("[2/6] Carregando dados OLTP no PostgreSQL...")
    carregar_oltp(fontes)

    # ── 3. DENORMALIZAR ──────────────────────
    print("[3/6] Denormalizando para star schema...")
    fontes_dn = denormalizar(fontes)

    # ── 4. TRANSFORM — dimensões ─────────────
    print("[4/6] Transformando dimensões...")
    df_datas_unificadas = pl.concat([
        fontes_dn["compras"].select("data"),
        fontes_dn["execucao"].select("data"),
        fontes_dn["estoque"].select("data"),
    ])
    dim_tempo        = build_dim_tempo(df_datas_unificadas)
    dim_projeto      = build_dim_projeto(fontes_dn["projetos"])
    dim_fornecedor   = build_dim_fornecedor(fontes_dn["fornecedores"])
    dim_material     = build_dim_material(fontes_dn["materiais"])
    dim_responsavel  = build_dim_responsavel(fontes_dn["execucao"])
    dim_tarefa       = build_dim_tarefa(fontes_dn["tarefas"])
    dim_solicitacao  = build_dim_solicitacao(fontes_dn["solicitacoes"])

    # ── 5. TRANSFORM — fatos ─────────────────
    print("[5/6] Transformando fatos...")
    fato_compras = build_fato_compras(
        fontes_dn["compras"],
        dim_projeto, dim_fornecedor,
        dim_material, dim_solicitacao, dim_tempo,
    )
    fato_execucao = build_fato_execucao_tarefas(
        fontes_dn["execucao"],
        dim_projeto, dim_tarefa, dim_responsavel, dim_tempo,
    )
    fato_estoque = build_fato_estoque_materiais(
        fontes_dn["estoque"],
        dim_projeto, dim_material, dim_tempo,
    )

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

    # ── 6. LOAD DW ───────────────────────────
    print("[6/6] Carregando star schema...")
    carregar_dw(dimensoes=dimensoes, fatos=fatos, pasta_saida="dw")
    carregar_dw_postgres(dimensoes=dimensoes, fatos=fatos)

    print("\n=== ETL concluído ===")


if __name__ == "__main__":
    main()
