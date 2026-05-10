# Bitbank Payment Saga

Projeto de estudo para implementar casos de uso de pagamento com arquitetura
hexagonal, comunicação por eventos e orquestração local com Docker Compose.

A implementação atual cobre os dois primeiros passos do fluxo:

1. `start_payment_service`: inicia uma transação de pagamento.
2. `debit_account_service`: debita a conta do cliente após receber o evento de
   pagamento iniciado.

Os próximos serviços planejados são:

```text
confirm_payment_service
reverse_payment_service
notify_merchant_service
notify_customer_service
issue_receipt_service
```

## Arquitetura

Cada serviço segue uma estrutura hexagonal básica:

```text
service/
├── src/
│   ├── domain/
│   ├── application/
│   │   ├── ports/
│   │   └── services/
│   ├── adapters/
│   │   ├── api/
│   │   ├── messaging/
│   │   └── persistence/
│   ├── configurator.py
│   └── main.py
├── tests/
├── specs/
├── requirements.txt
└── dockerfile
```

Regras principais:

- `domain` não depende de frameworks, banco ou mensageria.
- `application/ports` define contratos de entrada e saída.
- `application/services` implementa casos de uso.
- `adapters` contém FastAPI, RabbitMQ e SQLite.
- `configurator.py` monta as dependências concretas.

## Fluxo Implementado

```text
POST /payments/start
  -> start_payment_service cria Transaction com status STARTED
  -> salva em SQLite
  -> publica payment.started no RabbitMQ

RabbitMQ exchange: payments
  routing key: payment.started

Debit account consumer
  -> consome payment.started
  -> chama DebitAccountService
  -> busca Account por customer_id
  -> debita saldo quando possível
  -> publica debit.completed ou debit.failed
```

Eventos usados:

```text
payment.started
DebitCompleted -> debit.completed
DebitFailed    -> debit.failed
```

## Serviços

| Serviço | Porta | Responsabilidade |
| --- | --- | --- |
| `start_payment_service` | `8000` | Iniciar pagamento e publicar `PaymentStarted` |
| `debit_account_service` | `8001` | Debitar conta via API |
| `debit_account_consumer` | - | Consumir `payment.started` e executar débito |
| `rabbitmq` | `5672`, `15672` | Broker e painel de administração |

RabbitMQ Management:

```text
http://localhost:15672
user: bitbank
password: bitbank
```

## Subir Ambiente

```bash
docker compose up -d --build
```

Verificar containers:

```bash
docker compose ps
```

Acompanhar logs:

```bash
docker compose logs -f start_payment_service
docker compose logs -f debit_account_service
docker compose logs -f debit_account_consumer
```

Parar ambiente:

```bash
docker compose down
```

Remover volumes e bancos locais dos containers:

```bash
docker compose down -v
```

## Testar Start Payment

```bash
curl -X POST http://localhost:8000/payments/start \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": "customer-1",
    "merchant_id": "merchant-1",
    "amount": "50.00",
    "payment_method": "ACCOUNT_BALANCE"
  }'
```

Resposta esperada:

```json
{
  "transaction_id": "...",
  "status": "STARTED",
  "created_at": "..."
}
```

Esse comando também publica `payment.started` no RabbitMQ.

## Criar Conta Para Teste

Ainda não existe endpoint público para criação de conta. Para testar o caso
feliz do débito, crie uma conta diretamente no SQLite do container:

```bash
docker compose exec debit_account_service python - <<'PY'
from decimal import Decimal

from adapters.persistence.sqlite_account_repository import SQLiteAccountRepository
from domain.account import Account

repository = SQLiteAccountRepository("/data/debit_account.db")
account = Account.create(
    customer_id="customer-1",
    holder_name="Customer One",
    balance=Decimal("100.00"),
)
repository.save(account)
print(account.id)
PY
```

## Testar Debit Account Pela API

```bash
curl -X POST http://localhost:8001/accounts/debit \
  -H "Content-Type: application/json" \
  -d '{
    "transaction_id": "transaction-1",
    "customer_id": "customer-1",
    "amount": "50.00"
  }'
```

Resposta esperada com conta cadastrada:

```json
{
  "account_id": "...",
  "transaction_id": "transaction-1",
  "status": "COMPLETED",
  "reason": null
}
```

Resposta esperada sem conta cadastrada:

```json
{
  "account_id": null,
  "transaction_id": "transaction-1",
  "status": "FAILED",
  "reason": "ACCOUNT_NOT_FOUND"
}
```

## Testar Fluxo Pela Saga

1. Suba o ambiente.
2. Crie uma conta para `customer-1`.
3. Chame `POST /payments/start`.
4. Verifique o consumer:

```bash
docker compose logs -f debit_account_consumer
```

Com saldo suficiente, o consumer deve processar o evento `payment.started`,
debitar a conta e publicar `debit.completed`.

## Testes Automatizados

`start_payment_service`:

```bash
cd start_payment_service
make test
make lint
```

`debit_account_service`:

```bash
cd debit_account_service
make test
make lint
```

Ou, dentro de cada serviço:

```bash
make check
```

## Estado Atual

Implementado:

- `StartPayment` com FastAPI, SQLite e RabbitMQ publisher.
- `DebitAccount` com FastAPI, SQLite, RabbitMQ publisher e consumer.
- Testes unitários e de API para os dois serviços.
- Docker Compose com RabbitMQ e volumes persistentes.

Pendente:

- Endpoint público para criação/administração de contas.
- Outbox pattern para publicação transacional de eventos.
- Serviços seguintes da saga: confirmação, reversão, notificações e recibo.
