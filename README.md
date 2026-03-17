<img width="1300" height="240" src="./docs/media/banner-nexus.svg">

<br />
<span id="User-Standart">

# <p align="center">User-Standart</p>

<p align="center">
    <a href="#desafio">Desafio</a>  |  
    <a href="#solucao">Solução</a>  |   
    <a href="#product-backlog">Backlog do Produto</a>  |  
    <a href="#dor">DoR</a>  |  
    <a href="#dor">DoD</a>  |  
    <a href="#cronograma-de-sprints">Cronograma de Sprints</a>  |  
    <a href="#tecnologias">Tecnologias</a> | 
    <a href="#documentacao-api">Documentação API</a> | 
    <a href="#modelagem-de-banco-de-dados">Modelagem de Banco de Dados</a> | 
    <a href="#equipe">Equipe</a>
</p>

> Status do Projeto: **Em Desenvolvimento 🚧** <br /><br />
> Pasta de Documentação: [Link](https://github.com/User-Standart/API-5SEM/tree/main/docs) 📄 <br /><br />

---

<span id="desafio">

# 🏅 Desafio

A empresa **SIATT** executa projetos estratégicos que envolvem diversas áreas da organização, incluindo engenharia, aquisição de materiais, controle de horas técnicas e gestão de programas institucionais.

Atualmente, os dados operacionais estão distribuídos em diferentes sistemas e registros, dificultando a análise integrada das informações.

O desafio deste projeto consiste em **integrar, estruturar e analisar dados estratégicos de projetos**, permitindo que gestores tenham uma visão consolidada do consumo de recursos, evolução das atividades e histórico operacional dos programas da empresa.

---

<span id="solucao">

# 🏅 Solução

A solução proposta consiste na criação de uma **plataforma analítica de integração e exploração de dados**, capaz de consolidar informações provenientes de diferentes áreas da empresa.

O sistema permitirá:

- Integração de dados operacionais
- Estruturação das informações para análise
- Visualização histórica da evolução dos projetos
- Apoio à tomada de decisão estratégica

O objetivo é transformar dados dispersos em **informação estruturada e acessível**, permitindo uma gestão mais eficiente dos programas e projetos estratégicos da organização.

→ [Voltar ao topo](#User-Standart)

---

## 📋 Functional Requirements
<table>
    <tr>
        <th>ID</th>
        <th>Functional Requirement</th>
        <th>Description</th>
    </tr>
    <tr>
        <td>RF01</td>
        <td>ETL & Data Quality, DW</td>
        <td>The system must collect and consolidate data from different sources such as spreadsheets and CSV files, standardizing project IDs and organizing the information into a unified database.</td>
    </tr>
    <tr>
        <td>RF02</td>
        <td>Data validation and cleaning</td>
        <td>The system must identify inconsistencies in the imported data and perform validation and correction to ensure data quality before visualization.</td>
    </tr>
    <tr>
        <td>RF03</td>
        <td>Project cost visualization</td>
        <td>The system must display the total cost of each project through dashboards, allowing managers to identify projects consuming more resources than expected.</td>
    </tr>
    <tr>
        <td>RF04</td>
        <td>Delay risk indicator</td>
        <td>The system must display projects with a risk of delay using visual indicators and dashboards to help managers make faster decisions.</td>
    </tr>
    <tr>
        <td>RF05</td>
        <td>Cost vs execution dashboard</td>
        <td>The system must present a comparative dashboard relating project cost and execution progress to evaluate project performance.</td>
    </tr>
    <tr>
        <td>RF06</td>
        <td>Investment by program</td>
        <td>The system must display the total investment grouped by program, enabling strategic analysis of resource distribution.</td>
    </tr>
    <tr>
        <td>RF07</td>
        <td>Material consumption by project</td>
        <td>The system must display the consumption of materials by project in graphs or tables to understand how resources are being used.</td>
    </tr>
    <tr>
        <td>RF08</td>
        <td>Time spent by task and project</td>
        <td>The system must display the time spent on each task and project to allow productivity and effort analysis.</td>
    </tr>
    <tr>
        <td>RF09</td>
        <td>Analytical filters</td>
        <td>The system must allow filtering dashboards by program, project, task, material, order and time period to facilitate different levels of analysis.</td>
    </tr>
    <tr>
        <td>RF10</td>
        <td>Quick search</td>
        <td>The system must allow quick search for projects, materials and suppliers to locate specific information easily.</td>
    </tr>
    <tr>
        <td>RF11</td>
        <td>Data export</td>
        <td>The system must allow exporting dashboards and reports in formats such as CSV and PDF for sharing results in meetings and presentations.</td>
    </tr>
    <tr>
        <td>RF12</td>
        <td>Data visualization dashboards</td>
        <td>The system must provide analytical dashboards with graphs and tables to visualize consolidated project data.</td>
    </tr>
</table>

## 📋 Non-Functional Requirements

<table>
    <tr>
        <th>ID</th>
        <th>Non-Functional Requirements</th>
        <th>Description</th>
    </tr>
    <tr>
        <td>RNF01</td>
        <td>API Documentation</td>
        <td>The system must provide clear and detailed documentation for the API endpoints used to access consolidated data.</td>
    </tr>
    <tr>
        <td>RNF02</td>
        <td>Responsiveness</td>
        <td>The dashboards and visualization panels must be responsive and accessible from different devices such as desktop and mobile.</td>
    </tr>
    <tr>
        <td>RNF03</td>
        <td>User Manual</td>
        <td>The system must have a manual to guide users on how to use the system, including step-by-step tutorials for key features, usage tips and common troubleshooting.</td>
    </tr>
    <tr>
        <td>RNF04</td>
        <td>Data Quality</td>
        <td>The system must ensure data integrity and consistency through validation and treatment during the ETL process.</td>
    </tr>
    <tr>
        <td>RNF05</td>
        <td>Data Warehouse Modeling</td>
        <td>The system must implement a structured data model (DW – Data Warehouse) to support analytical queries and dashboards efficiently.</td>
    </tr>
    <tr>
        <td>RNF06</td>
        <td>Performance</td>
        <td>TThe system must allow fast access to analytical dashboards and queries even when handling large datasets.</td>
    </tr>
</table>

<br>

<span id="product-backlog">

## 🧵 Product Backlog

### 📋 Legenda dos Pacotes de Requisitos
| Pacote                | Requisitos cobertos    |
| ------------------    | ---------------------- |
| *ETL & Data Quality*  | RF01, RF02             |
| *Dashboards*          | RF03, RF04, RF05       |
| *Analytics*           | RF06, RF07, RF08       |
| *Filters & Search*    | RF09, RF10             |
| *Export*              | RNF11                  |
| *DW*                  | RNF01, RNF02           |
| *Docs & UX*           | RNF04, RNF05           |

</br> 

### ✅ Tabela de Itens do Backlog
| Rank | Pacotes de Requisitos        | User Story                                                                                                                                     | Perfil     | Prioridade | Sprint | Status     |
|------|------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------|------------|------------|--------|------------|
| 1 | ETL & Data Quality, DW | As a User, I want to gather and organize data from different systems and spreadsheets so that I can view all the information in a single place.| User    | 1          | 1      | 🔄 In Progress     |
| 2 | Dashboards, Docs & UX  | As a User, I want to visualize the total cost of each project in order to identify which ones are consuming more resources than expected.      | User    | 1           | 1     | 🔄 In Progress     |
| 3 | Dashboard              | As a User, I want to visualize projects at risk of delay so that I can make decisions quickly.                                                 | User    | 1          | 1      | 🔄 In Progress    |
| 4 | Dashboards, Analytics  | As a User, I want to visualize dashboards relating project cost and execution so that I can evaluate project performance.                      | User    | 2          | 1      | 🔄 In Progress|
| 5 | Analytics              |As a User, I want to visualize which program concentrates the highest investment so that I can support strategic decisions.                     | User    | 2          | 2      | ⏳ To Do    |
| 6 | Analytics              | As a User, I want to visualize material consumption per project so that I can understand where resources are being used.                       | User    | 2          | 2      | ⏳ To Do   |
| 7 | Analytics              | As a User, I want to visualize time spent per task and project so that I can evaluate effort and productivity.                                 | User    | 2          | 2      | ⏳ To Do  |
| 8 | Filters & Search       | As a User, I want to filter dashboards by program, project, task, material, order and period so that I can perform analyses at different levels.| User    | 2          | 2      | ⏳ To Do   |
| 9 | Filters & Search       |As a User, I want to quickly search for projects, materials and suppliers so that I can locate specific information easily.                     | User    | 3          | 2      | ⏳ To Do   |
| 10 | Export, Docs & UX     | As a User, I want to export reports and dashboards so that I can share results in meetings and presentations.                                  | User    | 3          | 3      | ⏳ To Do |


<br>

---

<span id="dor">

# 🏃‍  DoR - Definition of Ready

- User Stories com Critérios de Aceitação
- Subtarefas definidas
- Design definido
- Modelagem de Banco de Dados
- Definição da arquitetura do sistema
- Planejamento da Sprint

---

<span id="dod">

# 🏆 DoD - Definition of Done

- Código implementado
- Testes realizados
- Documentação atualizada
- Documentação da API
- Vídeos de apresentação das entregas

→ [Voltar ao topo](#User-Standart)

---

<span id="cronograma-de-sprints">

# 📅 Cronograma de Sprints

| Sprint | Período | Histórico |
|-|-|-|
| Sprint 1 | 16/03 - 05/04 | [Sprint 1 Docs](https://github.com/User-Standart/API-5SEM/tree/main/docs) |
| Sprint 2 | 13/04 - 03/05 | [Sprint 2 Docs](https://github.com/User-Standart/API-5SEM/tree/main/docs) |
| Sprint 3 | 11/05 - 31/05 | [Sprint 3 Docs](https://github.com/User-Standart/API-5SEM/tree/main/docs) |

→ [Voltar ao topo](#User-Standart)

---

<span id="tecnologias">

# 💻 Tecnologias

<p align="center">

<img src="https://img.shields.io/badge/Figma-F24E1E?style=for-the-badge&logo=figma&logoColor=white" />
<img src="https://img.shields.io/badge/Java-orange?style=for-the-badge&logo=openjdk&logoColor=white" />
<img src="https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D" />
<img src="https://img.shields.io/badge/Oracle-F80000?style=for-the-badge&logo=oracle&logoColor=white" />
<img src="https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white" />
<img src="https://img.shields.io/badge/Slack-4A154B?style=for-the-badge&logo=slack&logoColor=white" />
<img src="https://img.shields.io/badge/VS_Code-CED4DA?style=for-the-badge&logo=visual-studio-code&logoColor=0078D4" />
<img src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white" />
<img src="https://img.shields.io/badge/Jira-0052CC?style=for-the-badge&logo=jira&logoColor=white" />
<img src="https://img.shields.io/badge/Google%20Docs-CED4DA?style=for-the-badge&logo=google-docs&logoColor=0D96F6" />
<img src="https://img.shields.io/badge/Swagger-85EA2D?style=for-the-badge&logo=swagger&logoColor=black" />

</p>

→ [Voltar ao topo](#User-Standart)

---

<span id="documentacao-api">

# 📓 Documentação API

🚧 Em construção

→ [Voltar ao topo](#User-Standart)

---

<span id="modelagem-de-banco-de-dados">

# 🖥️ Modelagem de Banco de Dados

🚧 Em construção

→ [Voltar ao topo](#User-Standart)

---

<span id="equipe">

# 👥 Equipe

<div align="center">

| Função | Nome | LinkedIn & GitHub |
|------|------|----------------|
| Product Owner | Beatriz Sthefanny | [![Linkedin](https://img.shields.io/badge/Linkedin-blue?logo=Linkedin&logoColor=white)](https://www.linkedin.com/in/beatriz-santos-0b6773220/) [![GitHub](https://img.shields.io/badge/GitHub-111217?logo=github&logoColor=white)](https://github.com/BeatrizSantos00) |
| Scrum Master | Rafael Slivka | [![Linkedin](https://img.shields.io/badge/Linkedin-blue?logo=Linkedin&logoColor=white)](https://www.linkedin.com/in/rafael-lopes-slivka-07753326a/) [![GitHub](https://img.shields.io/badge/GitHub-111217?logo=github&logoColor=white)](https://github.com/rafaslivka) |
| Dev Team | Caio Osorio | [![Linkedin](https://img.shields.io/badge/Linkedin-blue?logo=Linkedin&logoColor=white)](https://www.linkedin.com/in/caio-o-a67224200/) [![GitHub](https://img.shields.io/badge/GitHub-111217?logo=github&logoColor=white)](https://github.com/User-Business) |
| Dev Team | Tiago Bernardo | [![Linkedin](https://img.shields.io/badge/Linkedin-blue?logo=Linkedin&logoColor=white)](https://www.linkedin.com/in/tiagobernardosantos/) [![GitHub](https://img.shields.io/badge/GitHub-111217?logo=github&logoColor=white)](https://github.com/TiagoBernardoSantos) |
| Dev Team | Victor Ryan | [![Linkedin](https://img.shields.io/badge/Linkedin-blue?logo=Linkedin&logoColor=white)](https://www.linkedin.com/in/victor-ryan-51738b261) [![GitHub](https://img.shields.io/badge/GitHub-111217?logo=github&logoColor=white)](https://github.com/yzvictorr) |
| Dev Team | Ali Mohamed Khodr | [![Linkedin](https://img.shields.io/badge/Linkedin-blue?logo=Linkedin&logoColor=white)](https://www.linkedin.com/in/alimohamedkhodr/) [![GitHub](https://img.shields.io/badge/GitHub-111217?logo=github&logoColor=white)](https://github.com/alimkhodr) |

</div>

→ [Voltar ao topo](#User-Standart)
