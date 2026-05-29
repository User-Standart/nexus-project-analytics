import http from 'k6/http';
import { sleep, check } from 'k6';

export const options = {
  // Teste de Estresse (Stress Testing) para encontrar o ponto de saturação
  stages: [
    { duration: '30s', target: 50 },    // Sobe para 50 usuários concorrentes
    { duration: '30s', target: 150 },   // Sobe para 150 usuários concorrentes
    { duration: '1m', target: 300 },    // Sobe para 300 usuários concorrentes (Testa o limite de threads)
    { duration: '1m', target: 500 },    // Sobe para 500 usuários concorrentes (Estresse alto)
    { duration: '30s', target: 0 },     // Desaquecimento
  ],
  thresholds: {
    // Monitoramento da taxa de erro. Se ultrapassar 5%, o threshold falha.
    http_req_failed: ['rate<0.05'],
    // 90% das requisições de login devem responder abaixo de 1.5s sob carga pesada
    http_req_duration: ['p(90)<1500'],
  },
};

const BASE_URL = __ENV.BASE_URL || 'http://localhost:8080';

export default function () {
  const url = `${BASE_URL}/api/auth/login`;
  
  // Corpo da requisição com dados simulados
  const payload = JSON.stringify({
    username: `user_${Math.floor(Math.random() * 20000)}`, // Simula usuários da lista de 20k
    password: 'password123',
  });

  const params = {
    headers: {
      'Content-Type': 'application/json',
    },
  };

  const res = http.post(url, payload, params);

  // Validações
  check(res, {
    'status is 200': (r) => r.status === 200,
    'has token': (r) => r.body.includes('token'),
  });

  // Intervalo curto entre as tentativas de login para maximizar a pressão de concorrência
  sleep(1);
}
