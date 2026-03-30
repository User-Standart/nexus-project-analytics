import os
import polars as pl


def carregar_dw(dimensoes: dict[str, pl.DataFrame],
                fatos: dict[str, pl.DataFrame],
                pasta_saida: str = "dw") -> None:
    """
    Salva todas as dimensões e fatos como CSVs na pasta do DW.
    Cria a pasta automaticamente se não existir.
    """
    os.makedirs(pasta_saida, exist_ok=True)

    # dimensões — ordem importa para integridade referencial
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
        dimensoes[nome].write_csv(f"{pasta_saida}/{nome}.csv")
        print(f"  [dim] {nome}.csv salvo")

    # fatos
    for nome, df in fatos.items():
        df.write_csv(f"{pasta_saida}/{nome}.csv")
        print(f"  [fat] {nome}.csv salvo")
