<html>
<body>
<!--StartFragment--><html><head></head><body><h1>📘 Documentação de Produto</h1>
<h2>🌐 Sobre a equipe</h2>
<p>A <strong>Nexus</strong> é uma plataforma analítica desenvolvida por uma equipe de estudantes da Fatec São José dos Campos, em parceria com a <strong>SIATT</strong>, para integrar, estruturar e explorar dados estratégicos de projetos.</p>
<p>A SIATT gerencia projetos estratégicos complexos distribuídos em múltiplos domínios organizacionais — engenharia, aquisição de materiais, apontamento de horas técnicas e supervisão de programas institucionais. Atualmente, os dados operacionais estão fragmentados em sistemas e registros dispersos, dificultando análises integradas e limitando a visibilidade sobre o desempenho dos projetos.</p>
<p>A plataforma transforma dados dispersos em <strong>inteligência estruturada e acessível</strong>, permitindo aos gestores acompanhar o consumo de recursos, o progresso de atividades e o histórico operacional dos programas da empresa com eficiência e transparência.</p>
<p>Esta documentação foi criada para oferecer uma referência completa sobre o uso da plataforma, suas funcionalidades e como maximizar seu potencial no apoio à tomada de decisão.</p>
<hr>
<h2>✅ Requisitos Funcionais (RFs)</h2>

<h3>📥 RF01 – ETL &amp; Qualidade de Dados / DW</h3>
<p>O sistema deve coletar e consolidar dados de múltiplas fontes — incluindo planilhas e arquivos CSV — padronizando identificadores de projetos e organizando todas as informações em um banco de dados unificado.</p>
<p>Fontes contempladas:</p>
<ul>
<li>📁 Projetos</li>
<li>📁 Programas</li>
<li>✅ Tarefas</li>
<li>⏱️ Horas trabalhadas</li>
<li>🛒 Pedidos de compra</li>
<li>📦 Materiais</li>
<li>🏢 Fornecedores</li>
</ul>
<h3>🔍 RF02 – Validação e Limpeza de Dados</h3>
<p>O sistema deve detectar inconsistências nos dados importados e aplicar procedimentos de validação e correção, garantindo a qualidade dos dados antes da visualização.</p>
<h3>💰 RF03 – Visualização de Custos por Projeto</h3>
<p>O sistema deve exibir o custo total de cada projeto em dashboards, permitindo que gestores identifiquem quais projetos estão consumindo mais recursos que o planejado.</p>
<h3>⚠️ RF04 – Indicador de Risco de Atraso</h3>
<p>O sistema deve apresentar projetos com risco de atraso por meio de indicadores visuais e dashboards, apoiando decisões gerenciais mais rápidas e embasadas.</p>
<h3>📊 RF05 – Dashboard Custo vs. Execução</h3>
<p>O sistema deve exibir um dashboard comparativo correlacionando o custo do projeto com o progresso de execução, para avaliação do desempenho geral.</p>
<h3>🏢 RF06 – Investimento por Programa</h3>
<p>O sistema deve exibir o investimento total agrupado por programa, possibilitando análise estratégica da distribuição de recursos na organização.</p>
<h3>📦 RF07 – Consumo de Materiais por Projeto</h3>
<p>O sistema deve exibir o consumo de materiais separado por projeto, utilizando gráficos ou tabelas para ilustrar a alocação e uso de recursos.</p>
<h3>⏱️ RF08 – Horas por Tarefa e Projeto</h3>
<p>O sistema deve exibir o tempo apontado por tarefa e por projeto, possibilitando análise de produtividade e esforço da equipe.</p>
<h3>🔎 RF09 – Filtros Analíticos</h3>
<p>O sistema deve suportar filtros nos dashboards por programa, projeto, tarefa, material, pedido e período de tempo, facilitando análises em múltiplos níveis.</p>
<h3>🔍 RF10 – Busca Rápida</h3>
<p>O sistema deve disponibilizar busca rápida de projetos, materiais e fornecedores, permitindo localizar informações específicas com o mínimo de esforço.</p>
<h3>📤 RF11 – Exportação de Dados</h3>
<p>O sistema deve suportar a exportação de dashboards e relatórios em formatos como <strong>CSV</strong> e <strong>PDF</strong>, facilitando o compartilhamento de resultados em reuniões e apresentações.</p>
<h3>📈 RF12 – Dashboards de Visualização de Dados</h3>
<p>O sistema deve fornecer dashboards analíticos com gráficos e tabelas para visualização consolidada dos dados de projetos.</p>
<hr>
<h2>🛡️ Requisitos Não Funcionais (RNFs)</h2>


ID | Requisito | Descrição
-- | -- | --
RNF01 | Documentação da API | O sistema deve fornecer documentação clara e completa de todos os endpoints de API utilizados para acesso aos dados consolidados.
RNF02 | Responsividade | Todos os dashboards e painéis de visualização devem ser totalmente responsivos e acessíveis em diferentes dispositivos, incluindo desktop e mobile.
RNF03 | Manual do Usuário | O sistema deve incluir um manual do usuário orientando sobre as principais funcionalidades, com tutoriais passo a passo, dicas de uso e solução de problemas comuns.
RNF04 | Qualidade de Dados | O sistema deve garantir integridade e consistência dos dados por meio de procedimentos robustos de validação e transformação durante o processo de ETL.
RNF05 | Modelagem do Data Warehouse | O sistema deve implementar um modelo de dados bem estruturado (Data Warehouse) capaz de suportar eficientemente consultas analíticas e dashboards.
RNF06 | Performance | O sistema deve proporcionar acesso rápido a dashboards e consultas analíticas, mesmo operando sobre grandes volumes de dados.

## ✨ Principais Funcionalidades

<details>
<summary>Clique aqui</summary>

### Sprint 1 - Visão de Projetos (Operacional)

#### 1. Cards de Resumo do Projeto

Objetivo: Exibir informações consolidadas do projeto selecionado.

| Card | Descrição | Cálculo |
|---|---|---|
| Custo Total | Valor total gasto no projeto | Soma de custo de horas técnicas + custo de materiais |
| Tempo Total | Total de horas trabalhadas | Soma de todas as horas apontadas no projeto |

Filtro: Seletor de projetos (busca por código/nome)

---

#### 2. Dashboard de Risco de Atraso

Objetivo: Sinalizar visualmente projetos com risco de não cumprir o prazo planejado.

| Desvio | Ação | Cor |
|---|---|---|
| ≤ 5% | Manter funcionamento | 🟢 |
| 5% - 15% | Monitorar | 🟡 |
| > 15% | Revisar urgentemente | 🔴 |

---

#### 3. Dashboard Custo vs. Execução

Objetivo: Correlacionar o progresso de execução com o consumo financeiro do projeto.

| Característica | Descrição |
|---|---|
| Tipo | Gráfico multi-linha |
| Eixo X | Tempo (data) |
| Eixo Y | Custo acumulado / % executado |
| Cada linha | Um projeto |
| Uso | Avaliar desempenho geral (avanço físico x avanço financeiro) |

---

#### 4. ETL & Integração de Dados

Objetivo: Coletar, padronizar e carregar dados de múltiplas fontes no Data Warehouse.

| Característica | Descrição |
|---|---|
| Fontes suportadas | Arquivos CSV e planilhas |
| Destino | Data Warehouse (PostgreSQL - modelo dimensional) |
| Transformações | Padronização de IDs, validação de inconsistências, deduplicação |
| Entidades integradas | Projetos, programas, tarefas, horas, materiais, pedidos, fornecedores |

---

### Sprint 2 - Visão de Programas (Tático)

#### 5. Cards de Resumo do Programa

Objetivo: Exibir informações consolidadas do programa selecionado.

| Card | Descrição | Cálculo |
|---|---|---|
| Custo Estimado | Valor planejado do programa | Soma de (estimativa_horas × custo_hora) |
| Custo Real | Valor efetivamente gasto | Soma de custo de horas + materiais |
| Horas Estimadas | Horas planejadas | Soma de estimativa_horas das tarefas |
| Horas Reais | Horas efetivamente trabalhadas | Soma de horas_trabalhadas |
| Total de Projetos | Quantidade de projetos | COUNT(projetos) do programa |

Filtro: Seletor de programas

---

#### 6. Consumo de Materiais por Projeto

Objetivo: Exibir materiais consumidos detalhados por projeto.

| Coluna | Descrição |
|---|---|
| Material | Nome e código do material |
| Projeto | Projeto onde o material foi utilizado |
| Quantidade | Quantidade consumida no projeto |
| Custo no Projeto | Quantidade × custo unitário do material |

Filtro: Projeto selecionado

---

#### 7. Horas por Tarefa e Projeto

Objetivo: Exibir a distribuição de horas apontadas por tarefa e por projeto.

| Característica | Descrição |
|---|---|
| Tipo | Gráfico de barras + evolução temporal (linha) |
| Eixo X | Funcionários / Tarefas |
| Eixo Y | Total de horas trabalhadas |
| Uso | Avaliar produtividade e esforço por equipe e projeto |

Filtro: Projeto / Programa selecionado

---

#### 8. Investimento por Programa

Objetivo: Exibir o total investido agrupado por programa para análise estratégica de recursos.

| Característica | Descrição |
|---|---|
| Tipo | Gráfico de barras |
| Eixo X | Programas (ex: MANSUP, MANSUP-ER, MAX 1.2 AC) |
| Eixo Y | Investimento total (R$) |
| Uso | Comparar distribuição de recursos entre programas |

---

#### 9. Filtros Analíticos

Objetivo: Permitir análises em múltiplos níveis com filtros interativos aplicados a todos os dashboards.

| Filtro | Aplicação | Sprint |
|---|---|---|
| Período (data inicial/final) | Todos os gráficos e tabelas | Sprint 2 |
| Programa | Dashboards táticos | Sprint 2 |
| Projeto | Dashboards operacionais | Sprint 2 |
| Tarefa | Tabelas de horas | Sprint 2 |
| Material | Tabelas de consumo | Sprint 2 |
| Pedido / Fornecedor | Tabelas de materiais | Sprint 2 |

---

#### 10. Busca Rápida

Objetivo: Localizar projetos, materiais e fornecedores com o mínimo de esforço.

| Característica | Descrição |
|---|---|
| Campos buscáveis | Projetos, materiais, fornecedores |
| Comportamento | Autocompletar com resultados em tempo real |
| Uso | Acesso direto a informações específicas sem navegação manual |

---

### Sprint 3 - Estratégico / Complementar

#### 11. Exportação de Dados

Objetivo: Permitir o compartilhamento de análises com outras áreas da organização.

| Formato | Aplicação |
|---|---|
| CSV | Tabelas e dados brutos |
| PDF | Dashboards e gráficos para apresentações |

Sprint: 3 (entrega complementar)

---

### Funcionalidades Transversais

#### Filtros Globais

| Filtro | Aplicação | Sprint |
|---|---|---|
| Período (data inicial/final) | Gráficos e tabelas | Sprint 2 |
| Status do Projeto | Tabelas e gráficos | Sprint 2 |
| Programa | Dashboards táticos | Sprint 2 |
| Material / Fornecedor | Tabelas de consumo e pedidos | Sprint 2 |

</details>
</body>
</html>