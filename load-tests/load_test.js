import http from 'k6/http';
import { sleep, check, group } from 'k6';

// Configurações do teste de carga
export const options = {
  // Define os estágios de crescimento (ramp-up), sustentação e redução (ramp-down) da carga
  stages: [
    { duration: '30s', target: 50 },   // Sobe de 0 a 50 usuários em 30 segundos (Warm up)
    { duration: '1m', target: 100 },   // Aumenta para 100 usuários por 1 minuto
    { duration: '2m', target: 200 },   // Carga sustentada com 200 usuários por 2 minutos (Massa crítica local)
    { duration: '30s', target: 0 },    // Desaquecimento (Ramp-down) em 30 segundos
  ],
  // Regras de sucesso do teste (se ultrapassadas, o teste é considerado falho)
  thresholds: {
    http_req_failed: ['rate<0.02'],    // A taxa de erro de requisições deve ser menor que 2%
    http_req_duration: ['p(95)<500'],  // 95% das requisições devem responder em menos de 500ms
  },
};

// Define a URL base da API a partir de variável de ambiente ou usa localhost por padrão
const BASE_URL = __ENV.BASE_URL || 'http://localhost:8080';

export default function () {
  const headers = { 'Content-Type': 'application/json' };

  // Grupo 1: Navegação pela aba de Projetos (Dimensão)
  group('Acesso a Dimensões (Projetos e Materiais)', function () {
    const resProjetos = http.get(`${BASE_URL}/api/dim/projetos`, { headers });
    check(resProjetos, {
      'status projetos é 200': (r) => r.status === 200,
      'dados retornados': (r) => r.body.length > 0,
    });

    sleep(1); // Simula o tempo que o usuário gasta olhando a tela

    const resMateriais = http.get(`${BASE_URL}/api/dim/materiais`, { headers });
    check(resMateriais, {
      'status materiais é 200': (r) => r.status === 200,
    });
  });

  sleep(2);

  // Grupo 2: Acesso ao Dashboard Analítico (Fatos)
  group('Visualização de Dashboards Analíticos', function () {
    // Requisição em lote (paralelo) simulando o carregamento dos cards do Dashboard
    const responses = http.batch([
      ['GET', `${BASE_URL}/api/fato/compras`, null, { headers }],
      ['GET', `${BASE_URL}/api/fato/execucao-tarefas`, null, { headers }],
      ['GET', `${BASE_URL}/api/programa/investimento`, null, { headers }]
    ]);

    check(responses[0], { 'fato compras carregou (200)': (r) => r.status === 200 });
    check(responses[1], { 'fato execucao carregou (200)': (r) => r.status === 200 });
    check(responses[2], { 'programa investimento carregou (200)': (r) => r.status === 200 });
  });

  sleep(3);

  // Grupo 3: Acesso ao Relatório de Compras (Purchases)
  group('Filtros de Compras', function () {
    const resPurchases = http.get(`${BASE_URL}/api/purchases`, { headers });
    check(resPurchases, {
      'status compras é 200': (r) => r.status === 200,
    });

    const resMetrics = http.get(`${BASE_URL}/api/purchases/metrics`, { headers });
    check(resMetrics, {
      'status métricas de compras é 200': (r) => r.status === 200,
    });
  });

  sleep(2); // Intervalo antes da próxima iteração do VU (Virtual User)
}
