import polars as pl


def extrair_fontes(pasta: str = ".") -> dict[str, pl.DataFrame]:
    """
    Lê todos os CSVs de origem e retorna um dicionário com os DataFrames brutos.
    Altere 'pasta' para apontar ao diretório onde seus CSVs estão.
    """
    return {
        "projetos":     pl.read_csv(f"{pasta}/projetos.csv"),
        "fornecedores": pl.read_csv(f"{pasta}/fornecedores.csv"),
        "materiais":    pl.read_csv(f"{pasta}/materiais.csv"),
        "solicitacoes": pl.read_csv(f"{pasta}/solicitacoes.csv"),
        "tarefas":      pl.read_csv(f"{pasta}/tarefas.csv"),
        "execucao":     pl.read_csv(f"{pasta}/execucao_tarefas.csv"),
        "compras":      pl.read_csv(f"{pasta}/compras.csv"),
        "estoque":      pl.read_csv(f"{pasta}/estoque.csv"),
    }
