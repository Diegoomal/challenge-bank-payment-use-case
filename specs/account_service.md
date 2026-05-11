# Account Service

## Descrição de Negócio

O `account_service` é responsável por criar contas financeiras para clientes.

Este serviço pertence ao contexto de Conta e representa a entrada administrativa para abertura de contas que poderão participar do fluxo de pagamento.

Ele recebe uma solicitação HTTP, cria uma nova `Account` com status `ACTIVE`, persiste a conta e publica o evento `account.created`.

## Bounded Context

Conta.

## Ubiquitous Language

- Account: conta financeira de um cliente.
- AccountId: identificador único da conta.
- Customer: cliente dono da conta.
- AccountHolder: titular da conta.
- Balance: saldo disponível da conta.
- AccountStatus: estado atual da conta.
- InitialDeposit: valor inicial depositado na conta.
- AccountCreated: evento que informa que uma conta foi criada.

## Aggregate Root

### Account

A `Account` é o Aggregate Root do contexto de Conta.

Ela controla os dados principais da conta e garante que uma conta seja criada em estado válido.

## Estados da Conta

- ACTIVE
- INACTIVE
- CLOSED

## Invariantes

- Uma conta deve possuir um `account_id` único.
- Uma conta deve possuir um `customer_id`.
- Uma conta deve possuir um titular válido.
- Uma conta recém-criada deve iniciar com status `ACTIVE`.
- O depósito inicial não pode ser negativo.
- Um cliente não deve possuir mais de uma conta ativa.
- Uma conta não deve iniciar com saldo negativo.

## Caso de Uso Principal

### CreateAccount

Responsável por criar uma nova conta financeira para um cliente.

Entrada esperada:

- customer_id
- account_holder
- initial_deposit

Saída esperada:

- account_id
- customer_id
- status
- created_at

## Domain Events Consumidos

Este serviço não consome eventos de domínio.

Ele é iniciado por uma chamada HTTP externa.

## Domain Events Publicados

### AccountCreated

Publicado quando uma conta é criada com sucesso.

Payload sugerido:

- account_id
- customer_id
- account_holder
- initial_deposit
- status
- created_at

## Portas

### AccountRepository

Responsável por salvar e recuperar contas.

### EventPublisher

Responsável por publicar eventos de domínio.

## Responsabilidades

Este serviço deve:

- Receber uma solicitação de criação de conta.
- Validar os dados da conta.
- Verificar se o cliente já possui conta ativa.
- Criar uma nova conta com status `ACTIVE`.
- Persistir a conta.
- Publicar o evento `account.created`.

Este serviço não deve:

- Iniciar pagamento.
- Debitar conta.
- Creditar conta.
- Confirmar pagamento.
- Reverter pagamento.
- Notificar cliente ou merchant.
- Emitir comprovante.