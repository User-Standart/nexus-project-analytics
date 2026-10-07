# Análise dos CSVs

> **Responsável:** User-Standart Team

---

## 1. Visão Geral

| Tabela                    | Linhas | Colunas | Observações                          |
|---------------------------|--------|---------|--------------------------------------|
| `programas`               | 3      | 8       | Tabela pequena, dados mestres        |
| `projetos`                | 100    | 9       | Tabela central do OLTP               |
| `tarefas_projeto`         | 100    | 9       | Relacionada 1:N a projetos           |
| `tempo_tarefas`           | 100    | 5       | Granularidade diária por usuário     |
| `materiais`               | 100    | 7       | Catálogo de materiais                |
| `fornecedores`            | 100    | 7       | Cadastro de fornecedores             |
| `solicitacoes_compra`     | 100    | 8       | Origem do processo de compra         |
| `pedidos_compra`          | 100    | 8       | Relacionado 1:1 a solicitações       |
| `compras_projeto`         | 100    | 4       | Tabela de rateio pedido → projeto    |
| `empenho_materiais`       | 100    | 5       | Reserva de material por projeto      |
| `estoque_materiais_projeto` | 100  | 5       | Posição de estoque por projeto/local |

**Total de registros de dados:** 1.003 linhas  

---

## 2. Análise por Tabela

---

### 2.1 `programas`

**Colunas:**

| Campo              | Tipo       | Categoria   | Descrição                          |
|--------------------|------------|-------------|------------------------------------|
| `id`               | int        | ID / PK     | Identificador interno              |
| `codigo_programa`  | varchar    | ID / Código | Ex: `MANSUP`, `MAX12AC`            |
| `nome_programa`    | varchar    | Descritivo  | Nome legível do programa           |
| `gerente_programa` | varchar    | Descritivo  | Nome do gerente responsável        |
| `gerente_tecnico`  | varchar    | Descritivo  | Nome do gerente técnico            |
| `data_inicio`      | date       | Data        | Início do programa                 |
| `data_fim_prevista`| date       | Data        | Previsão de encerramento           |
| `status`           | varchar    | Problema    | `Concluído`, `Em andamento`        |

**Observações:**
- Apenas **3 registros** — tabela de dados mestres estável.
- Nenhum valor nulo.
- `status` possui apenas 2 valores distintos no conjunto atual.

---

### 2.2 `projetos`

**Colunas:**

| Campo              | Tipo       | Categoria   | Descrição                                   |
|--------------------|------------|-------------|---------------------------------------------|
| `id`               | int        | ID / PK     | Identificador interno                       |
| `codigo_projeto`   | varchar    | ID / Código | Ex: `PRJ001`                                |
| `nome_projeto`     | varchar    | Descritivo  | Nome do projeto                             |
| `programa_id`      | int        | ID / FK     | FK → `programas.id`                         |
| `responsavel`      | varchar    | Descritivo  | Nome do responsável                         |
| `custo_hora`       | numeric    | Métrica     | Custo por hora (R$) — min: 75,24, max: 148,48, média: 115,13 |
| `data_inicio`      | date       | Data        | Range: 2022-01-11 → 2025-02-12              |
| `data_fim_prevista`| date       | Data        | Range: 2022-09-28 → 2026-03-29              |
| `status`           | varchar    | Problema    | `Planejamento`, `Em andamento`, `Concluído`, `Suspenso` |

**Distribuição por programa:**

| `programa_id` | Qtd projetos |
|---------------|--------------|
| 1             | 38           |
| 2             | 33           |
| 3             | 29           |

**Observações:**
- Nenhum valor nulo.
- Integridade referencial com `programas` ✅ — zero órfãos.
- `responsavel` é texto livre; será fonte da `dim_responsavel` no DW.

---

### 2.3 `tarefas_projeto`

**Colunas:**

| Campo              | Tipo       | Categoria   | Descrição                                       |
|--------------------|------------|-------------|-------------------------------------------------|
| `id`               | int        | ID / PK     | Identificador interno                           |
| `codigo_tarefa`    | varchar    | ID / Código | Ex: `TSK001`                                    |
| `projeto_id`       | int        | ID / FK     | FK → `projetos.id`                              |
| `titulo`           | varchar    | Descritivo  | Descrição da tarefa                             |
| `responsavel`      | varchar    | Descritivo  | Nome do responsável                             |
| `estimativa_horas` | int        | Métrica     | Horas planejadas para a tarefa                  |
| `data_inicio`      | date       | Data        | Range: 2022-03-16 → 2025-07-01                  |
| `data_fim_prevista`| date       | Data        | Range: 2022-04-03 → 2025-09-05                  |
| `status`           | varchar    | Problema    | `Não iniciada`, `Em andamento`, `Bloqueada`, `Concluída` |

**Distribuição de status:**

| Status         | Qtd |
|----------------|-----|
| Não iniciada   | 29  |
| Em andamento   | 27  |
| Bloqueada      | 23  |
| Concluída      | 21  |

**Observações:**
- Nenhum valor nulo.
- Integridade referencial com `projetos` ✅ — zero órfãos.

---

### 2.4 `tempo_tarefas`

**Colunas:**

| Campo              | Tipo       | Categoria   | Descrição                                        |
|--------------------|------------|-------------|--------------------------------------------------|
| `id`               | int        | ID / PK     | Identificador interno                            |
| `tarefa_id`        | int        | ID / FK     | FK → `tarefas_projeto.id`                        |
| `usuario`          | varchar    | Descritivo  | Nome do usuário que lançou as horas              |
| `data`             | date       | Data        | Range: 2022-03-23 → 2025-09-01                   |
| `horas_trabalhadas`| numeric    | Métrica     | Horas lançadas — min: 0,54h, max: 9,9h, média: 4,51h |

**Observações:**
- Nenhum valor nulo.
- Integridade referencial com `tarefas_projeto` ✅ — zero órfãos.
- `usuario` é campo livre — pode diferir do `responsavel` da tarefa (apontamento por outros membros).
- Será a **principal fonte de fatos** para `fato_execucao_tarefas`.

---

### 2.5 `materiais`

**Colunas:**

| Campo            | Tipo       | Categoria   | Descrição                              |
|------------------|------------|-------------|----------------------------------------|
| `id`             | int        | ID / PK     | Identificador interno                  |
| `codigo_material`| varchar    | ID / Código | Ex: `MAT001`                           |
| `descricao`      | varchar    | Descritivo  | Descrição técnica do componente        |
| `categoria`      | varchar    | Descritivo  | 15 categorias distintas (ver abaixo)   |
| `fabricante`     | varchar    | Descritivo  | Nome do fabricante                     |
| `custo_estimado` | numeric    | Métrica     | Custo unitário estimado (R$)           |
| `status`         | varchar    | Problema    | `Ativo`, `Inativo`, `Obsoleto`         |

**Categorias de materiais:**

| Categoria              | Qtd |
|------------------------|-----|
| Sensor                 | 13  |
| Capacitor              | 10  |
| Diodo                  | 10  |
| Indutor                | 10  |
| Conector               | 7   |
| Relé                   | 7   |
| Regulador de Tensão    | 6   |
| LED                    | 6   |
| Transistor             | 6   |
| MOSFET                 | 6   |
| Display                | 5   |
| Transformador          | 5   |
| Resistor               | 4   |
| CI Digital             | 3   |
| CI Analógico           | 2   |

**Observações:**
- Nenhum valor nulo.
- Materiais `Obsoleto` e `Inativo` devem ser tratados na carga da `dim_material` — decidir se entram ou ficam marcados com flag.

---

### 2.6 `fornecedores`

**Colunas:**

| Campo              | Tipo       | Categoria   | Descrição                                     |
|--------------------|------------|-------------|-----------------------------------------------|
| `id`               | int        | ID / PK     | Identificador interno                         |
| `codigo_fornecedor`| varchar    | ID / Código | Ex: `FOR001`                                  |
| `razao_social`     | varchar    | Descritivo  | Nome legal do fornecedor                      |
| `cidade`           | varchar    | Descritivo  | Cidade sede                                   |
| `estado`           | char(2)    | Descritivo  | UF — todos os 100 registros são `SP`          |
| `categoria`        | varchar    | Descritivo  | Tipo de fornecimento (ex: "Materiais de Solda") |
| `status`           | varchar    | Problema    | `Ativo`, `Inativo`, `Bloqueado`               |

**Observações:**
- Nenhum valor nulo.
- Campo `estado` homogêneo (`SP` em 100% dos registros) — baixo valor analítico, mas deve ser mantido.
- Fornecedores `Bloqueado` participam de pedidos existentes — **não filtrar na carga do DW**.

---

### 2.7 `solicitacoes_compra`

**Colunas:**

| Campo               | Tipo       | Categoria   | Descrição                                      |
|---------------------|------------|-------------|------------------------------------------------|
| `id`                | int        | ID / PK     | Identificador interno                          |
| `numero_solicitacao`| varchar    | ID / Código | Ex: `SC0001`                                   |
| `projeto_id`        | int        | ID / FK     | FK → `projetos.id`                             |
| `material_id`       | int        | ID / FK     | FK → `materiais.id`                            |
| `quantidade`        | int        | Métrica     | Quantidade solicitada                          |
| `data_solicitacao`  | date       | Data        | Range: 2022-03-10 → 2025-08-19                 |
| `prioridade`        | varchar    | Descritivo  | `Crítica`, `Alta`, `Média`, `Baixa`            |
| `status`            | varchar    | Problema    | `Aprovada`, `Pendente`, `Rejeitada`, `Cancelada` |

**Distribuição de prioridade:**

| Prioridade | Qtd |
|------------|-----|
| Alta       | 29  |
| Crítica    | 27  |
| Média      | 23  |
| Baixa      | 21  |

**Distribuição de status:**

| Status    | Qtd |
|-----------|-----|
| Rejeitada | 28  |
| Cancelada | 26  |
| Aprovada  | 26  |
| Pendente  | 20  |

**Observações:**
- Nenhum valor nulo.
- Integridade referencial com `projetos` e `materiais` ✅ — zero órfãos.
- Alto índice de rejeições/cancelamentos (~54%) — dado analiticamente relevante para `fato_compras`.

---

### 2.8 `pedidos_compra`

**Colunas:**

| Campo                  | Tipo       | Categoria   | Descrição                                        |
|------------------------|------------|-------------|--------------------------------------------------|
| `id`                   | int        | ID / PK     | Identificador interno                            |
| `numero_pedido`        | varchar    | ID / Código | Ex: `PC0001`                                     |
| `solicitacao_id`       | int        | ID / FK     | FK → `solicitacoes_compra.id`                    |
| `fornecedor_id`        | int        | ID / FK     | FK → `fornecedores.id`                           |
| `data_pedido`          | date       | Data        | Range: 2022-03-13 → 2025-08-25                   |
| `data_previsao_entrega`| date       | Data        | Range: 2022-03-20 → 2025-10-05                   |
| `valor_total`          | numeric    | Métrica     | Valor total do pedido (R$)                       |
| `status`               | varchar    | Problema    | `Aberto`, `Enviado`, `Entregue`, `Parcialmente Entregue`, `Cancelado` |

**Distribuição de status:**

| Status                  | Qtd |
|-------------------------|-----|
| Cancelado               | 22  |
| Aberto                  | 20  |
| Parcialmente Entregue   | 20  |
| Entregue                | 19  |
| Enviado                 | 19  |

**Observações:**
- Nenhum valor nulo.
- Integridade referencial com `solicitacoes_compra` e `fornecedores` ✅ — zero órfãos.
- Relação **1:1 com solicitações** (cada pedido origina-se de uma solicitação).
- O `valor_total` do pedido é rateado em `compras_projeto` quando alocado a múltiplos projetos.

---

### 2.9 `compras_projeto`

**Colunas:**

| Campo             | Tipo       | Categoria   | Descrição                                         |
|-------------------|------------|-------------|---------------------------------------------------|
| `id`              | int        | ID / PK     | Identificador interno                             |
| `pedido_compra_id`| int        | ID / FK     | FK → `pedidos_compra.id`                          |
| `projeto_id`      | int        | ID / FK     | FK → `projetos.id`                                |
| `valor_alocado`   | numeric    | Métrica     | Valor do pedido alocado para este projeto (R$)    |

**Observações:**
- Nenhum valor nulo.
- Integridade referencial com `pedidos_compra` e `projetos` ✅ — zero órfãos.
- Tabela de **rateio**: um mesmo pedido pode ter `valor_alocado` distribuído entre múltiplos projetos.
- No ETL do DW: `valor_alocado` vai para `fato_compras.valor_alocado_projeto` e `valor_total` do pedido vai para `fato_compras.valor_total_pedido`.

---

### 2.10 `empenho_materiais`

**Colunas:**

| Campo                 | Tipo       | Categoria   | Descrição                              |
|-----------------------|------------|-------------|----------------------------------------|
| `id`                  | int        | ID / PK     | Identificador interno                  |
| `projeto_id`          | int        | ID / FK     | FK → `projetos.id`                     |
| `material_id`         | int        | ID / FK     | FK → `materiais.id`                    |
| `quantidade_empenhada`| int        | Métrica     | Quantidade reservada                   |
| `data_empenho`        | date       | Data        | Range: 2022-02-16 → 2025-09-05         |

**Observações:**
- Nenhum valor nulo.
- Integridade referencial com `projetos` e `materiais` ✅ — zero órfãos.
- Será fonte para `fato_estoque_materiais.quantidade_empenhada`.

---

### 2.11 `estoque_materiais_projeto`

**Colunas:**

| Campo         | Tipo       | Categoria   | Descrição                                      |
|---------------|------------|-------------|------------------------------------------------|
| `id`          | int        | ID / PK     | Identificador interno                          |
| `projeto_id`  | int        | ID / FK     | FK → `projetos.id`                             |
| `material_id` | int        | ID / FK     | FK → `materiais.id`                            |
| `quantidade`  | int        | Métrica     | Quantidade disponível em estoque               |
| `localizacao` | varchar    | Descritivo  | 6 locais distintos (ver abaixo)                |

**Localizações:**

| Localização      |
|------------------|
| Almoxarifado     |
| Depósito Central |
| Laboratório A    |
| Laboratório B    |
| Laboratório C    |
| Linha Protótipo  |

**Observações:**
- Nenhum valor nulo.
- Integridade referencial com `projetos` e `materiais` ✅ — zero órfãos.
- Tabela sem dimensão de tempo — representa **posição atual** do estoque. No DW, será associada à `dim_tempo` na carga (data de snapshot).

---

## 3. Integridade Referencial — Resumo

| Relação                                          | Órfãos |
|--------------------------------------------------|--------|
| `projetos.programa_id` → `programas.id`          | ✅ 0   |
| `tarefas_projeto.projeto_id` → `projetos.id`     | ✅ 0   |
| `tempo_tarefas.tarefa_id` → `tarefas_projeto.id` | ✅ 0   |
| `solicitacoes_compra.projeto_id` → `projetos.id` | ✅ 0   |
| `solicitacoes_compra.material_id` → `materiais.id` | ✅ 0 |
| `pedidos_compra.solicitacao_id` → `solicitacoes_compra.id` | ✅ 0 |
| `pedidos_compra.fornecedor_id` → `fornecedores.id` | ✅ 0  |
| `compras_projeto.pedido_compra_id` → `pedidos_compra.id` | ✅ 0 |
| `compras_projeto.projeto_id` → `projetos.id`     | ✅ 0   |
| `empenho_materiais.projeto_id` → `projetos.id`   | ✅ 0   |
| `empenho_materiais.material_id` → `materiais.id` | ✅ 0   |
| `estoque_materiais_projeto.projeto_id` → `projetos.id` | ✅ 0 |
| `estoque_materiais_projeto.material_id` → `materiais.id` | ✅ 0 |

**Resultado: integridade referencial 100% íntegra nos dados de origem.**

---

## 4. Mapeamento Fonte → DW

| Tabela de Origem                          | Destino no DW                                      |
|-------------------------------------------|----------------------------------------------------|
| `programas` + `projetos`                  | `dim_projeto`                                      |
| `tarefas_projeto`                         | `dim_tarefa`                                       |
| `tarefas_projeto.responsavel` + `tempo_tarefas.usuario` | `dim_responsavel`                |
| `materiais`                               | `dim_material`                                     |
| `fornecedores`                            | `dim_fornecedor`                                   |
| `solicitacoes_compra` + `pedidos_compra`  | `dim_solicitacao`                                  |
| Todas as colunas de data                  | `dim_tempo` (geração sintética do range completo)  |
| `solicitacoes_compra` + `pedidos_compra` + `compras_projeto` | `fato_compras`            |
| `tempo_tarefas` + `tarefas_projeto`       | `fato_execucao_tarefas`                            |
| `estoque_materiais_projeto` + `empenho_materiais` | `fato_estoque_materiais`                 |

---

## 5. Pontos de Atenção para o ETL

1. **`dim_tempo`** deve ser gerada sinteticamente cobrindo o range **2022-01-01 → 2027-12-31** para contemplar todas as datas de previsão.

2. **`dim_responsavel`** unifica dois campos de texto livre: `projetos.responsavel`, `tarefas_projeto.responsavel` e `tempo_tarefas.usuario`. Aplicar `DISTINCT` + normalização de nomes antes da carga.

3. **`dim_solicitacao`** é uma dimensão degenerada — desnormaliza dados de `solicitacoes_compra` e `pedidos_compra` em uma única dimensão para evitar múltiplos joins na fato.

4. **`estoque_materiais_projeto`** não possui data — na carga do DW, usar a data de execução do pipeline como `sk_tempo` (snapshot).

5. **Materiais com `status = Obsoleto/Inativo`** participam de empenhos e estoques existentes — incluir na `dim_material` com flag de status, sem filtrar.

6. **`compras_projeto.valor_alocado`** pode ser menor que `pedidos_compra.valor_total` quando o pedido é rateado entre projetos — ambos os valores devem ser carregados na `fato_compras`.

7. **Fornecedores com `status = Bloqueado`** aparecem em pedidos históricos — incluir na `dim_fornecedor`.
