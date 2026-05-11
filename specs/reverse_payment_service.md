# Reverse Payment Service

## Descrição de Negócio

O `reverse_payment_service` é responsável por reverter uma transação de pagamento quando alguma etapa financeira da saga falhar.

Este serviço pertence ao contexto de Pagamento e representa a etapa de compensação da saga.

Ele consome os eventos `debit.failed` ou `credit.failed`, valida se a transação pode ser revertida, altera o status para `REVERSED` e publica o evento `payment.reversed`.

## Bounded Context

Pagamento.

## Ubiquitous Language

- Payment: pagamento solicitado por um cliente.
- Transaction: registro principal do pagamento.
- TransactionId: identificador único da transação.
- TransactionStatus: estado atual da transação.
- Reversal: ação de compensação aplicada quando o pagamento não pode ser concluído.
- ReversalReason: motivo da reversão.
- DebitFailed: evento que informa que o débito falhou.
- CreditFailed: evento que informa que o crédito falhou.

## Aggregate Root

### Transaction

A `Transaction` é o Aggregate Root do contexto de Pagamento.

Ela controla o ciclo de vida do pagamento e garante que uma transação só seja revertida em estado válido.

## Estados da Transação

- STARTED
- CONFIRMED
- REVERSED
- FAILED

## Invariantes

- Uma transação só pode ser revertida se estiver com status `STARTED` ou `PROCESSING`.
- Uma transação já confirmada não deve ser revertida por falha de débito ou crédito.
- Uma transação já revertida não deve ser revertida novamente.
- Uma transação falhada não deve ser confirmada.
- A reversão deve estar associada a um `transaction_id`.
- A reversão deve registrar o motivo da falha.
- A reversão deve ser idempotente por `transaction_id`.

## Caso de Uso Principal

### ReversePayment

Responsável por reverter uma transação após falha no débito ou no crédito.

Entrada esperada:

- transaction_id
- customer_id
- merchant_id
- amount
- reason
- occurred_at

Saída esperada:

- transaction_id
- status
- reversal_reason
- reversed_at

## Domain Events Consumidos

### DebitFailed

Consumido quando o débito da conta do cliente falha.

Payload esperado:

- transaction_id
- customer_id
- merchant_id
- amount
- reason
- failed_at

### CreditFailed

Consumido quando o crédito na conta do recebedor falha.

Payload esperado:

- transaction_id
- customer_id
- merchant_id
- amount
- reason
- failed_at

## Domain Events Publicados

### PaymentReversed

Publicado quando a transação de pagamento é revertida com sucesso.

Payload sugerido:

- transaction_id
- customer_id
- merchant_id
- amount
- reason
- reversed_at

## Portas

### TransactionRepository

Responsável por recuperar e salvar transações.

### EventPublisher

Responsável por publicar eventos de domínio.

## Responsabilidades

Este serviço deve:

- Consumir os eventos `debit.failed` e `credit.failed`.
- Buscar a transação pelo `transaction_id`.
- Validar se a transação pode ser revertida.
- Alterar o status da transação para `REVERSED`.
- Registrar o motivo da reversão.
- Persistir a alteração.
- Publicar o evento `payment.reversed`.

Este serviço não deve:

- Criar transações.
- Debitar conta.
- Creditar conta.
- Confirmar pagamento.
- Notificar cliente ou lojista.
- Emitir comprovante.