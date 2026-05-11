# API Gateway

## Descrição de Negócio

O `api_gateway` é responsável por expor uma entrada única para os clientes externos acessarem os serviços da plataforma.

Este componente não pertence a um Bounded Context específico. Ele atua como camada de entrada da aplicação, roteando requisições HTTP para os serviços internos corretos.

Ele centraliza o acesso externo, simplifica a comunicação com os clientes e protege os serviços internos de exposição direta.

## Bounded Context

Não possui Bounded Context próprio.

O `api_gateway` é um componente de infraestrutura/aplicação que conecta clientes externos aos Bounded Contexts internos.

## Ubiquitous Language

- API Gateway: ponto único de entrada da aplicação.
- Route: caminho HTTP exposto para o cliente.
- Upstream Service: serviço interno que recebe a requisição.
- Request: solicitação feita pelo cliente.
- Response: resposta retornada ao cliente.
- CorrelationId: identificador usado para rastrear uma requisição entre serviços.
- Authentication: validação de identidade do cliente.
- Authorization: validação de permissão de acesso.

## Responsabilidade Principal

O `api_gateway` deve receber requisições externas e encaminhá-las para o serviço interno responsável.

Exemplos:

- `/api/v1/accounts` encaminha para `account_service`
- `/api/v1/payments/start` encaminha para `start_payment_service`

## Casos de Uso Principais

### RouteAccountRequests

Responsável por encaminhar requisições de conta para o `account_service`.

### RoutePaymentRequests

Responsável por encaminhar requisições de pagamento para o `start_payment_service`.

## Regras

- O gateway deve expor uma API pública simples e consistente.
- O gateway deve esconder os endereços internos dos serviços.
- O gateway deve encaminhar headers relevantes, como `correlation_id`.
- O gateway deve retornar respostas padronizadas para o cliente.
- O gateway não deve conter regra de negócio de domínio.
- O gateway não deve acessar diretamente bancos de dados dos serviços.
- O gateway não deve publicar eventos de domínio.
- O gateway não deve executar lógica de pagamento, conta, notificação ou comprovante.

## Portas / Integrações

### HTTP Client

Responsável por chamar os serviços internos.

### Request Router

Responsável por mapear rotas externas para serviços internos.

### Error Handler

Responsável por padronizar respostas de erro.

## Responsabilidades

Este componente deve:

- Expor rotas públicas HTTP.
- Encaminhar requisições para os serviços internos.
- Propagar `correlation_id`.
- Padronizar respostas de erro.
- Centralizar o ponto de entrada da aplicação.
- Facilitar autenticação e autorização no futuro.
- Evitar exposição direta dos serviços internos.

Este componente não deve:

- Criar contas diretamente.
- Iniciar pagamentos diretamente no domínio.
- Debitar conta.
- Creditar conta.
- Confirmar pagamento.
- Reverter pagamento.
- Notificar cliente ou merchant.
- Emitir comprovante.
- Acessar bancos internos dos serviços.
- Publicar eventos de domínio.