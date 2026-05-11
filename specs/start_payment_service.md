# Start Payment Service

## Descrição de Negócio

O `start_payment_service` é responsável por iniciar uma transação de pagamento.

Este serviço pertence ao contexto de Pagamento e representa a primeira etapa da saga de pagamento.

Ele recebe uma solicitação de pagamento, cria uma nova `Transaction` com status `STARTED`, persiste a transação e publica o evento `payment.started`.

## Bounded Context

Pagamento.

## Ubiquitous Language

- Payment: pagamento solicitado por um cliente.
- Transaction: registro principal do pagamento.
- TransactionId: identificador único da transação.
- TransactionStatus: estado atual da transação.
- PaymentMethod: método utilizado para realizar o pagamento.
- Amount: valor monetário da transação.
- Customer: cliente pagador.
- Merchant: recebedor do pagamento.
- PaymentStarted: evento que informa que uma transação de pagamento foi iniciada.

## Aggregate Root

### Transaction

A `Transaction` é o Aggregate Root do contexto de pagamento.

Ela controla o início do ciclo de vida do pagamento e garante que uma transação seja criada em estado válido.

## Estados da Transação

- STARTED
- CONFIRMED
- REVERSED
- FAILED

## Invariantes

- Uma transação deve possuir um `transaction_id` único.
- Uma transação deve possuir `customer_id`.
- Uma transação deve possuir `merchant_id`.
- Uma transação deve possuir valor maior que zero.
- Uma transação deve possuir um método de pagamento válido.
- Uma transação recém-criada deve iniciar com status `STARTED`.
- Uma transação não deve ser confirmada no momento da criação.
- Uma transação não deve ser revertida no momento da criação.

## Caso de Uso Principal

### StartPayment

Responsável por iniciar uma nova transação de pagamento.

Entrada esperada:

- customer_id
- merchant_id
- amount
- payment_method

Saída esperada:

- transaction_id
- status
- created_at

## Domain Events Consumidos

Este serviço não consome eventos de domínio.

Ele é iniciado por uma chamada HTTP externa.

## Domain Events Publicados

### PaymentStarted

Publicado quando uma transação de pagamento é criada com sucesso.

Payload sugerido:

- transaction_id
- customer_id
- merchant_id
- amount
- payment_method
- occurred_at

## Portas

### TransactionRepository

Responsável por salvar e recuperar transações.

### EventPublisher

Responsável por publicar eventos de domínio.

## Responsabilidades

Este serviço deve:

- Receber uma solicitação de início de pagamento.
- Criar uma nova transação.
- Validar os dados iniciais do pagamento.
- Persistir a transação com status `STARTED`.
- Publicar o evento `payment.started`.

Este serviço não deve:

- Debitar conta.
- Creditar conta.
- Confirmar pagamento.
- Reverter pagamento.
- Notificar cliente ou lojista.
- Emitir comprovante.