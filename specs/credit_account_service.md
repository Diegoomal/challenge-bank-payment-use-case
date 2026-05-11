# Credit Account Service

## Descrição de Negócio

O `credit_account_service` é responsável por creditar a conta do recebedor após o débito da conta do cliente ser realizado com sucesso.

Este serviço pertence ao contexto de Conta e representa a etapa em que o valor transferido é disponibilizado para o merchant/recebedor.

Ele consome o evento `debit.completed`, valida se a conta do recebedor existe, realiza o crédito, registra o lançamento contábil e publica `credit.completed` ou `credit.failed`.

## Bounded Context

Conta.

## Ubiquitous Language

- Account: conta financeira do recebedor.
- AccountId: identificador único da conta.
- AccountHolder: titular da conta.
- Balance: saldo disponível da conta.
- AccountingEntry: lançamento contábil gerado por uma movimentação.
- Credit: operação de entrada de saldo.
- Merchant: recebedor do pagamento.
- DebitCompleted: evento que informa que o débito do pagador foi realizado com sucesso.

## Aggregate Root

### Account

A `Account` é o Aggregate Root do contexto de Conta.

Ela controla o saldo e garante que operações de crédito sejam registradas corretamente.

## Entidades

### AccountingEntry

Representa um lançamento contábil associado a uma operação de crédito.

## Estados / Resultados do Crédito

- COMPLETED
- FAILED

## Invariantes

- Uma conta do recebedor deve existir para receber o crédito.
- O valor do crédito deve ser maior que zero.
- Todo crédito aprovado deve gerar um lançamento contábil.
- Uma operação de crédito deve estar associada a um `transaction_id`.
- A mesma transação não deve ser creditada mais de uma vez.
- A operação deve ser idempotente por `transaction_id`.

## Caso de Uso Principal

### CreditAccount

Responsável por creditar o saldo da conta do recebedor.

Entrada esperada:

- transaction_id
- customer_id
- merchant_id
- amount
- debited_at

Saída esperada:

- account_id
- transaction_id
- status
- reason

## Domain Events Consumidos

### DebitCompleted

Consumido quando o débito da conta do cliente foi realizado com sucesso.

Payload esperado:

- transaction_id
- account_id
- customer_id
- merchant_id
- amount
- debited_at

## Domain Events Publicados

### CreditCompleted

Publicado quando o crédito é realizado com sucesso.

Payload sugerido:

- transaction_id
- account_id
- customer_id
- merchant_id
- amount
- credited_at

### CreditFailed

Publicado quando o crédito não pode ser realizado.

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

- Consumir o evento `debit.completed`.
- Buscar a conta pelo `merchant_id`.
- Validar se a conta do recebedor existe.
- Creditar o valor na conta.
- Registrar o lançamento contábil.
- Persistir a conta atualizada.
- Publicar o evento `credit.completed` em caso de sucesso.
- Publicar o evento `credit.failed` em caso de falha.

Este serviço não deve:

- Criar transações de pagamento.
- Debitar conta do pagador.
- Confirmar pagamento.
- Reverter pagamento.
- Notificar cliente ou lojista.
- Emitir comprovante.