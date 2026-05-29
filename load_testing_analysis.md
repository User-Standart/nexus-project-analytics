# 📊 Relatório de Teste de Carga & Estimativa de Custos de Infraestrutura
## Projeto: User-Standart (Monitoramento & Análise de Custos e Prazos)

Este documento apresenta uma análise técnica e comercial detalhada para responder aos questionamentos sobre a execução de **testes de carga** e os **custos associados de escalabilidade** para a plataforma **User-Standart**, considerando o patamar de **20.000 usuários**.

---

## 1. Alinhamento de Escopo: O que significa "20.000 usuários"?

Antes de dimensionar servidores ou estimar preços, é fundamental separar os conceitos de volume de usuários. O custo e a infraestrutura mudam drasticamente dependendo de como esses 20.000 usuários se comportam:

| Métrica | Definição | Impacto na Infraestrutura | Foco do Teste de Carga |
| :--- | :--- | :--- | :--- |
| **Usuários Cadastrados / Totais** | Total de contas criadas no banco de dados. | Impacto direto apenas no tamanho de armazenamento do banco de dados (muito barato). | Baixo |
| **Usuários Ativos Diários (DAU)** | 20.000 usuários únicos que acessam o sistema ao longo de um dia de 24 horas. | Tráfego distribuído. Estima-se um pico de **200 a 500 acessos simultâneos** nos horários mais movimentados. | Médio |
| **Usuários Simultâneos / Concorrentes (VUs)** | **20.000 usuários clicando e fazendo requisições ao mesmo tempo**, no mesmo segundo. | Tráfego extremo. Exige infraestrutura de alta performance com múltiplos servidores redundantes e banco de dados robusto. | **Altíssimo** |

> [!IMPORTANT]
> Para uma aplicação corporativa de monitoramento de projetos internos (como a SIATT), o cenário mais provável é de **20.000 usuários cadastrados / ativos diários**, com picos menores de concorrência. No entanto, detalhamos abaixo os custos tanto para o cenário **Realista (Corporativo)** quanto para o cenário **Extremo (Simultaneidade)** para responder plenamente ao questionamento do professor.

---

## 2. Estratégia de Teste de Carga com Grafana k6

Dada a stack do projeto (Go no backend, Nuxt/JS no frontend, PostgreSQL no banco, e Grafana/Prometheus no monitoramento), a ferramenta recomendada para os testes de carga é o **Grafana k6**.

### Por que o k6?
1. **Escrito em Go:** Mesma linguagem do backend do projeto, gerando ótima performance de execução.
2. **Scripts em JavaScript:** Fácil escrita de cenários para quem desenvolve em Nuxt/Vue.
3. **Integração Nativa:** Envia métricas do teste diretamente para o **Prometheus** e **Grafana** do próprio projeto, centralizando a visualização no mesmo painel que vocês já configuraram.

### Exemplo Prático de Script k6 (`load-test.js`)
Este script simula usuários fazendo requisições para a API de projetos da User-Standart, aumentando gradativamente a carga até o pico desejado.

```javascript
import http from 'k6/http';
import { sleep, check } from 'k6';

// Configuração do cenário de escalabilidade
export const options = {
  stages: [
    { duration: '5m', target: 500 },  // Sobe gradativamente até 500 usuários ativos
    { duration: '10m', target: 500 }, // Mantém 500 usuários fazendo requisições (estresse)
    { duration: '5m', target: 20000 },// Sobe para o pico de 20.000 usuários simultâneos
    { duration: '5m', target: 20000 },// Mantém o pico por 5 minutos
    { duration: '5m', target: 0 },    // Reduz para 0 (desaquecimento)
  ],
  thresholds: {
    http_req_failed: ['rate<0.01'],   // Menos de 1% de requisições falhas aceitáveis
    http_req_duration: ['p(95)<300'], // 95% das requisições devem responder em menos de 300ms
  },
};

export default function () {
  // Simula requisição ao endpoint de listagem de projetos
  const res = http.get('http://backend-url:8080/api/projetos');
  
  check(res, {
    'status is 200': (r) => r.status === 200,
    'body has projects': (r) => r.body.includes('id'),
  });

  sleep(1); // Tempo de espera simulado entre cliques do usuário
}
```

---

## 3. Estimativa de Custos de Infraestrutura (Nuvem AWS)

Abaixo está o dimensionamento e a estimativa de custos na AWS (Amazon Web Services), dividida nos dois cenários de negócios.

### Cenário A: Realista (20.000 Usuários Cadastrados / ~1.000 Concorrentes no Pico)
Ideal para a operação real da plataforma na SIATT.

*   **Frontend (Nuxt SSR):** Hospedado em containers redundantes leves no AWS ECS Fargate (2 instâncias de 0.25 vCPU / 0.5 GB RAM).
*   **Backend (Go REST API):** Go é extremamente performático. 2 instâncias leves de 0.5 vCPU / 1 GB RAM dão conta com folga do tráfego corporativo.
*   **Banco de Dados (RDS PostgreSQL):** 1 instância `db.t4g.medium` (2 vCPU, 4 GB RAM) com Multi-AZ para tolerância a falhas.
*   **Rede e Balanceamento (ALB):** 1 Application Load Balancer para distribuir as requisições.
*   **Armazenamento de Logs (Loki + S3):** Armazenamento em nuvem otimizado para logs do Loki.

| Componente AWS | Especificação | Custo Mensal (USD) | Custo Mensal (BRL)* |
| :--- | :--- | :--- | :--- |
| **AWS ECS Fargate (Frontend)** | 2 Tasks (0.25 vCPU, 0.5 GB RAM) | $18.00 | R$ 90,00 |
| **AWS ECS Fargate (Backend Go)** | 2 Tasks (0.5 vCPU, 1 GB RAM) | $32.00 | R$ 160,00 |
| **AWS RDS PostgreSQL** | 1x `db.t4g.medium` (Multi-AZ) + 50GB GP3 | $68.00 | R$ 340,00 |
| **AWS ALB (Load Balancer)** | 1x Application Load Balancer | $22.50 | R$ 112,50 |
| **CloudFront (CDN) / S3** | Cache estático e transferência de dados (~100GB) | $12.00 | R$ 60,00 |
| **Observabilidade (Prometheus/Loki)** | Armazenamento de métricas e logs no S3 | $15.00 | R$ 75,00 |
| **TOTAL MENSAL ESTIMADO** | **Cenário Realista** | **~$167.50** | **~R$ 837,50** |

---

### Cenário B: Extremo (20.000 Usuários Concorrentes Ativos Simultaneamente)
Cenário de teste de estresse severo ou aplicação pública de altíssimo tráfego.

*   **Necessidade de Cache:** Para atingir essa concorrência em queries analíticas (dashboards de custos e prazos do Data Warehouse), um cache (Redis) é obrigatório, caso contrário o banco de dados PostgreSQL irá travar independente do seu tamanho.
*   **Escalonamento Automático (Autoscaling):** Servidores do backend e frontend aumentam dinamicamente conforme a demanda.

| Componente AWS | Especificação | Custo Mensal (USD) | Custo Mensal (BRL)* |
| :--- | :--- | :--- | :--- |
| **AWS ECS Fargate (Frontend)** | Auto-scaling (4 a 12 Tasks) | ~$120.00 | R$ 600,00 |
| **AWS ECS Fargate (Backend Go)** | Auto-scaling (6 a 20 Tasks) | ~$350.00 | R$ 1.750,00 |
| **AWS RDS PostgreSQL** | Principal (`db.m6g.2xlarge` - 8 vCPU, 32GB RAM) + 1 Read Replica (`db.m6g.2xlarge`) + 200GB GP3 Storage | ~$890.00 | R$ 4.450,00 |
| **AWS ElastiCache (Redis)** | Cache de queries analíticas (`cache.m6g.large`) | ~$130.00 | R$ 650,00 |
| **AWS ALB (Load Balancer)** | 1x Application Load Balancer (alto tráfego LCU) | ~$90.00 | R$ 450,00 |
| **CloudFront (CDN) / S3** | Transferência de dados de alta escala (~2 TB/mês) | ~$180.00 | R$ 900,00 |
| **Observabilidade (Prometheus/Loki)** | Ingestão e retenção massiva de telemetria | ~$120.00 | R$ 600,00 |
| **TOTAL MENSAL ESTIMADO** | **Cenário de Pico Simultâneo** | **~$1,880.00** | **~R$ 9.400,00** |

*\*Nota: Conversão estimada considerando câmbio de US$ 1.00 = R$ 5,00. Os valores não incluem impostos locais de faturamento (como IOF e PIS/COFINS incidentes sobre serviços de nuvem estrangeiros).*

---

## 4. Custos para Executar o Teste de Carga

Rodar um teste que simula 20.000 usuários não pode ser feito a partir de uma máquina local. A internet e o processador do testador seriam o gargalo. Existem duas opções de custo para rodar os testes:

### Opção 1: k6 Cloud (SaaS Gerenciado)
O plano gratuito do k6 Cloud suporta até 500 usuários simultâneos. Para testar 20.000 usuários simultâneos com infraestrutura distribuída gerenciada pela própria Grafana Labs:
*   **Custo:** Exige assinatura de planos corporativos personalizados ou compra de créditos avulsos. Um teste de pico pontual de 20k VUs custa em média entre **$150 USD a $300 USD (cerca de R$ 750,00 a R$ 1.500,00)** por campanha de testes executada.
*   **Vantagem:** Sem dor de cabeça de infraestrutura, relatórios analíticos prontos e detalhados.

### Opção 2: k6 Localmente Distribuído (Auto-hospedado em instâncias temporárias)
Subir instâncias virtuais na AWS temporariamente (durante o teste) para gerar a carga.
*   **Custo de Máquina (AWS EC2):** Seria necessário criar cerca de 5 instâncias temporárias `c5.2xlarge` (8 vCPUs, 16 GB RAM) em diferentes zonas geográficas para atuar como geradores de carga do k6.
    *   Custo por hora de execução dessas instâncias: ~$1.70 USD por hora.
    *   **Custo total de infraestrutura:** Menos de **$10 USD (R$ 50,00)** para várias horas de testes.
*   **Desvantagem:** Exige esforço e tempo de engenharia (DevOps) para configurar a infraestrutura de carga distribuída, coletar os arquivos de log e consolidar os dados.

---

## 5. Como Monitorar e Validar os Testes (O Papel da Observabilidade)

Como o projeto já possui **Prometheus, Grafana, Loki e Promtail** provisionados, esses componentes são as estrelas durante a simulação de carga. O cliente ou o time de DevOps utilizará esses painéis para responder:

1.  **Gargalo de CPU/Memória:** Qual serviço começa a falhar primeiro? (O backend Go ou o frontend Nuxt?).
2.  **Métricas do Banco de Dados:** O PostgreSQL está sofrendo com travas de conexão (connection pooling)? As consultas analíticas demoram mais de 500ms?
3.  **Logs de Erros (Loki):** Os servidores estão retornando status `502 Bad Gateway` ou `504 Gateway Timeout` sob carga?
4.  **Uso de Recursos Real:** Ajuda a calibrar o autoscaling na nuvem, evitando gastos desnecessários de servidores sobressalentes.

---

### Resumo para Apresentação ao Professor:
*   **Ferramenta recomendada:** Grafana k6 (sinergia técnica com Go, JS e a stack de monitoramento do projeto).
*   **Custo de Infraestrutura Realista (Uso Corporativo normal):** ~$170 USD/mês (cerca de R$ 850/mês).
*   **Custo de Infraestrutura Extrema (20k simultâneos):** ~$1.880 USD/mês (cerca de R$ 9.400/mês), onde o banco de dados e as replicas de leitura correspondem a 50% do custo.
*   **Custo do Teste de Carga:** De R$ 50,00 (esforço manual de DevOps na AWS) a R$ 1.500,00 (usando a ferramenta oficial k6 Cloud SaaS).
