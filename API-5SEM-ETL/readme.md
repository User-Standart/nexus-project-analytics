# API-5SEM-ETL

Pipeline ETL para o Data Warehouse da User-Standart, construído com Python e Polars.

---

# Como rodar o projeto

## Pré-requisitos

- Python 3.11+
- pip

## Linux

1. Instale o Python e o pip
```
sudo apt update
```
```
sudo apt install python3 python3-pip
```

## Windows

1. Baixe e instale o Python 3.11+ pelo site oficial
```
https://www.python.org/downloads
```
Durante a instalação, marque a opção **"Add Python to PATH"**.

## Passos seguintes (para ambos Linux e Windows)

1. Clone o repositório
```
git clone https://github.com/User-Standart/API-5SEM-ETL.git
```
```
cd API-5SEM-ETL
```

2. Instale as dependências
```
pip install polars
```

3. Adicione os CSVs de origem na pasta `data/`

   Os seguintes arquivos são esperados:
   - `projetos.csv`
   - `programas.csv`
   - `tarefas_projeto.csv`
   - `tempo_tarefas.csv`
   - `materiais.csv`
   - `fornecedores.csv`
   - `solicitacoes_compra.csv`
   - `pedidos_compra.csv`
   - `compras_projeto.csv`
   - `empenho_materiais.csv`
   - `estoque_materiais_projeto.csv`

4. Execute o pipeline
```
python etl/main.py
```

Os arquivos de saída serão salvos na pasta `dw/`.

---

# Estrutura do projeto

O projeto segue uma estrutura de pastas **modular**, onde os arquivos são organizados com base em sua responsabilidade dentro do pipeline.

```
API-5SEM-ETL/
│
├── docs/                        # Documentação e artefatos de modelagem
│   ├── csv_analysis.md          # Análise dos CSVs de origem (estrutura, integridade, mapeamento)
│   ├── modelo_relacional.png    # Modelo relacional OLTP
│   └── modelo_estrela.png       # Modelo estrela OLAP
│
├── data/                        # CSVs de origem (não versionados)
│   └── .gitkeep
│
├── etl/                         # Pipeline ETL
│   ├── main.py                  # Ponto de entrada — orquestra o pipeline completo
│   ├── extract.py               # Leitura dos CSVs de origem
│   ├── load.py                  # Escrita das tabelas no /dw
│   └── transform/
│       ├── __init__.py          # Expõe todas as funções de transformação
│       ├── dimensoes.py         # Funções build_dim_* para as 7 dimensões
│       └── fatos.py             # Funções build_fato_* para as 3 tabelas fato
│
├── dw/                          # Gerado pelo pipeline (não versionado)
│
├── .gitignore
└── README.md
```

### Para que serve cada arquivo

- **`main.py`** — único arquivo que você executa. Chama extract, transform e load na ordem correta.
- **`extract.py`** — lê os CSVs da pasta `data/` e retorna os DataFrames brutos.
- **`load.py`** — salva os DataFrames processados como CSVs na pasta `dw/`.
- **`transform/dimensoes.py`** — constrói as 7 dimensões (tempo, projeto, fornecedor, etc.).
- **`transform/fatos.py`** — constrói as 3 tabelas fato com joins nas dimensões e tratamento de surrogate keys nulas.
- **`transform/__init__.py`** — torna `transform` um pacote Python, permitindo o `from transform import ...` no `main.py`.

---

# Acordos do projeto

- Código em inglês
- Mensagens de commit em inglês

# Padrão de commits e branches

Seguimos o Conventional Commits.

## Commits
`<tipo>(<id-da-issue>): <breve descrição em inglês>`

Exemplo: `feat(etl): add surrogate key null handling to fact tables`

## Branch
`feature/<id-da-issue>-<breve-descricao-em-ingles>`

Exemplo: `feature/8-star-schema-modeling-and-etl`
