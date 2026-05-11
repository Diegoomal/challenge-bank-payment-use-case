# Debit Account Service

## Descrição de Negócio

O `debit_account_service` é responsável por debitar a conta do cliente após uma transação de pagamento ser iniciada.

Este serviço pertence ao contexto de Conta e representa a etapa em que o saldo do pagador é reservado/retirado para continuidade da saga de pagamento.

Ele consome o evento `payment.started`, valida se a conta possui saldo suficiente, realiza o débito, registra o lançamento contábil e publica `debit.completed` ou `debit.failed`.

## Bounded Context

Conta.

## Ubiquitous Language

- Account: conta financeira do cliente.
- AccountId: identificador único da conta.
- AccountHolder: titular da conta.
- Balance: saldo disponível da conta.
- AccountingEntry: lançamento contábil gerado por uma movimentação.
- Debit: operação de retirada de saldo.
- InsufficientBalance: erro de domínio quando o saldo é menor que o valor solicitado.
- PaymentStarted: evento que informa que uma transação de pagamento foi iniciada.

## Aggregate Root

### Account

A `Account` é o Aggregate Root do contexto de Conta.

Ela controla o saldo e garante que nenhuma operação deixe a conta em estado inválido.

## Entidades

### AccountingEntry

Representa um lançamento contábil associado a uma operação de débito.

## Estados / Resultados do Débito

- COMPLETED
- FAILED

## Invariantes

- Uma conta não pode possuir saldo negativo.
- Um débito só pode ocorrer se houver saldo suficiente.
- O valor do débito deve ser maior que zero.
- Todo débito aprovado deve gerar um lançamento contábil.
- Uma operação de débito deve estar associada a um `transaction_id`.
- A mesma transação não deve ser debitada mais de uma vez.
- A operação deve ser idempotente por `transaction_id`.

## Caso de Uso Principal

### DebitAccount

Responsável por debitar o saldo da conta do cliente.

Entrada esperada:

- transaction_id
- customer_id
- merchant_id
- amount
- payment_method
- occurred_at

Saída esperada:

- account_id
- transaction_id
- status
- reason

## Domain Events Consumidos

### PaymentStarted

Consumido quando uma transação de pagamento é iniciada.

Payload esperado:

- transaction_id
- customer_id
- merchant_id
- amount
- payment_method
- occurred_at

## Domain Events Publicados

### DebitCompleted

Publicado quando o débito é realizado com sucesso.

Payload sugerido:

- transaction_id
- account_id
- customer_id
- merchant_id
- amount
- debited_at

### DebitFailed

Publicado quando o débito não pode ser realizado.

Payload sugerido:

- transaction_id
- customer_id
- merchant_id
- amount
- reason
- failed_at

## Portas

### AccountRepository

Responsável por recuperar e salvar contas.

### EventPublisher

Responsável por publicar eventos de domínio.

## Responsabilidades

Este serviço deve:

- Consumir o evento `payment.started`.
- Buscar a conta pelo `customer_id`.
- Validar se a conta existe.
- Validar se há saldo suficiente.
- Debitar o valor da conta.
- Registrar o lançamento contábil.
- Persistir a conta atualizada.
- Publicar o evento `debit.completed` em caso de sucesso.
- Publicar o evento `debit.failed` em caso de falha.

Este serviço não deve:

- Criar transações de pagamento.
- Creditar conta do recebedor.
- Confirmar pagamento.
- Reverter pagamento.
- Notificar cliente ou lojista.
- Emitir comprovante.