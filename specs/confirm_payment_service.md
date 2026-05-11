# Confirm Payment Service

## Descrição de Negócio

O `confirm_payment_service` é responsável por confirmar uma transação de pagamento após o crédito na conta do recebedor ser realizado com sucesso.

Este serviço pertence ao contexto de Pagamento e representa a etapa em que o pagamento deixa de ser apenas iniciado e passa a ser considerado confirmado.

Ele consome o evento `credit.completed`, valida se a transação pode ser confirmada, altera o status para `CONFIRMED` e publica o evento `payment.confirmed`.

## Bounded Context

Pagamento.

## Ubiquitous Language

- Payment: pagamento solicitado por um cliente.
- Transaction: registro principal do pagamento.
- TransactionId: identificador único da transação.
- TransactionStatus: estado atual da transação.
- Confirmation: confirmação de que o pagamento foi concluído.
- CreditCompleted: evento que informa que o crédito ao recebedor foi realizado com sucesso.

## Aggregate Root

### Transaction

A `Transaction` é o Aggregate Root do contexto de Pagamento.

Ela controla o ciclo de vida do pagamento e garante que uma transação só seja confirmada em estado válido.

## Estados da Transação

- STARTED
- CONFIRMED
- REVERSED
- FAILED

## Invariantes

- Uma transação só pode ser confirmada se estiver com status `STARTED`.
- Uma transação já confirmada não pode ser confirmada novamente.
- Uma transação revertida não pode ser confirmada.
- Uma transação falhada não pode ser confirmada.
- A confirmação deve estar associada a um `transaction_id`.
- A confirmação só pode ocorrer após o crédito ao recebedor ser realizado com sucesso.
- A confirmação deve ser idempotente por `transaction_id`.

## Caso de Uso Principal

### ConfirmPayment

Responsável por confirmar uma transação após o crédito ser concluído.

Entrada esperada:

- transaction_id
- customer_id
- merchant_id
- account_id
- amount
- credited_at

Saída esperada:

- transaction_id
- status
- confirmed_at

## Domain Events Consumidos

### CreditCompleted

Consumido quando o crédito na conta do recebedor foi realizado com sucesso.

Payload esperado:

- transaction_id
- customer_id
- merchant_id
- account_id
- amount
- credited_at

## Domain Events Publicados

### PaymentConfirmed

Publicado quando o pagamento é confirmado com sucesso.

Payload sugerido:

- transaction_id
- customer_id
- merchant_id
- amount
- confirmed_at

## Portas

### TransactionRepository

Responsável por recuperar e salvar transações.

### EventPublisher

Responsável por publicar eventos de domínio.

## Responsabilidades

Este serviço deve:

- Consumir o evento `credit.completed`.
- Buscar a transação pelo `transaction_id`.
- Validar se a transação pode ser confirmada.
- Alterar o status da transação para `CONFIRMED`.
- Persistir a alteração.
- Publicar o evento `payment.confirmed`.

Este serviço não deve:

- Criar transações.
- Debitar conta.
- Creditar conta.
- Reverter pagamento.
- Notificar cliente ou lojista.
- Emitir comprovante.