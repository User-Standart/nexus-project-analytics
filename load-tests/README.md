# 🧪 Guia de Teste de Carga — User-Standart

Este diretório contém o cenário de teste de carga automatizado utilizando o **k6** para simular usuários concorrentes acessando a API do backend da User-Standart.

---

## 🛠️ Pré-requisitos

Para rodar os testes, você precisará ter o **k6** instalado na sua máquina local.

### Como instalar no Windows:

#### Opção A (Via PowerShell - Recomendado):
Execute o comando abaixo com o gerenciador de pacotes padrão do Windows (Winget):
```powershell
winget install k6
```

#### Opção B (Instalação Manual):
1. Baixe o instalador MSI na página oficial: [k6 Releases](https://github.com/grafana/k6/releases).
2. Execute o instalador e adicione o k6 ao PATH do seu sistema.

---

## 🚀 Como Executar os Testes

Com os serviços Docker do projeto rodando (`docker compose up`), abra o terminal na raiz deste repositório e execute os comandos abaixo.

### 1. Teste Rápido (Validação/Smoke Test)
Simula apenas 1 usuário ativo por 1 iteração para validar se todos os endpoints estão respondendo corretamente.
```powershell
k6 run --vus 1 --duration 10s load-tests/load_test.js
```

### 2. Teste de Carga Local (Padrão)
Executa o cenário configurado em [load_test.js](./load_test.js), que gradualmente sobe a carga até **200 usuários simultâneos** locais.
```powershell
k6 run load-tests/load_test.js
```

### 3. Alterando a URL do Servidor
Se quiser testar a aplicação hospedada em outro servidor ou porta:
```powershell
k6 run -e BASE_URL=http://url-do-servidor:porta load-tests/load_test.js
```

---

## 📊 Como Validar e Analisar os Resultados

### 1. Pelo Terminal (Console Output)
Ao finalizar o teste, o k6 imprimirá um relatório detalhado contendo:
*   `http_req_failed`: Porcentagem de requisições falhas (deve ser 0% ou muito próximo de 0%).
*   `http_req_duration`: Latência das requisições (mínimo, média, mediana, percentis p90 e p95). O ideal é que o `p(95)` fique abaixo de **500ms**.
*   `vus`: Número de usuários simultâneos ativos durante o pico.
*   `checks`: Quantidade de asserções que passaram vs falharam (validação se os dados vieram vazios ou se a rota quebrou).

### 2. Integrado à Observabilidade Local (Grafana + Prometheus)
O k6 possui integração nativa para enviar os resultados de performance diretamente para o Prometheus do seu projeto. 

Para rodar o teste enviando os dados para a stack de monitoramento local:
```powershell
k6 run -o experimental-prometheus-rw load-tests/load_test.js
```
*(Nota: Certifique-se de que a porta de ingestão do Prometheus esteja mapeada e exposta no seu `docker-compose.monitoring.yml`)*

Após rodar o comando:
1. Acesse o seu painel do Grafana (geralmente em `http://localhost:3000` ou a porta configurada).
2. Crie ou importe um dashboard de K6 (ex: painel ID `18030` no Grafana Labs).
3. Visualize as curvas de carga, RPS (Requisições por segundo) e tempo de resposta diretamente do lado dos logs coletados pelo Promtail/Loki.
