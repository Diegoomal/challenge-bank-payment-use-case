# Issue Receipt Service

## Descrição de Negócio

O `issue_receipt_service` é responsável por emitir o comprovante após uma transação de pagamento ser confirmada.

Este serviço pertence ao contexto de Comprovante e representa a etapa de geração do documento da saga de pagamento.

Ele consome o evento `payment.confirmed`, cria um comprovante com um snapshot dos dados da transação confirmada, persiste o comprovante e publica o evento `receipt.issued`.

## Bounded Context

Comprovante.

## Ubiquitous Language

- Receipt: documento que comprova um pagamento confirmado.
- ReceiptId: identificador único do comprovante.
- TransactionData: snapshot dos dados da transação confirmada.
- IssuingStatus: estado atual da emissão do comprovante.
- PaymentConfirmed: evento que informa que o pagamento foi confirmado.

## Aggregate Root

### Receipt

O `Receipt` é o Aggregate Root do contexto de Comprovante.

Ele controla o ciclo de vida da emissão e garante que apenas um comprovante válido seja emitido para cada transação.

## Estados do Comprovante

- PENDING
- ISSUED
- FAILED

## Invariantes

- Um comprovante só pode ser emitido após o pagamento ser confirmado.
- Um comprovante deve estar associado a um `transaction_id`.
- Uma transação deve possuir no máximo um comprovante válido.
- O comprovante deve conter um snapshot dos dados da transação.
- O comprovante não deve depender diretamente da entidade `Transaction` de outro serviço.
- A emissão deve ser idempotente por `transaction_id`.
- Se já existir comprovante para a transação, o serviço deve retornar o existente ou ignorar o evento duplicado.

## Caso de Uso Principal

### IssueReceipt

Responsável por emitir o comprovante após o pagamento ser confirmado.

Entrada esperada:

- transaction_id
- customer_id
- merchant_id
- amount
- confirmed_at

Saída esperada:

- receipt_id
- transaction_id
- status
- issued_at

## Domain Events Consumidos

### PaymentConfirmed

Consumido quando a transação de pagamento é confirmada.

Payload esperado:

- transaction_id
- customer_id
- merchant_id
- amount
- confirmed_at

## Domain Events Publicados

### ReceiptIssued

Publicado quando o comprovante é emitido com sucesso.

Payload sugerido:

- receipt_id
- transaction_id
- customer_id
- merchant_id
- amount
- issued_at

## Portas

### ReceiptRepository

Responsável por salvar e recuperar comprovantes.

### ReceiptGenerator

Responsável por gerar os dados ou documento do comprovante.

### EventPublisher

Responsável por publicar eventos de domínio.

## Responsabilidades

Este serviço deve:

- Consumir o evento `payment.confirmed`.
- Criar um comprovante para a transação confirmada.
- Armazenar um snapshot dos dados da transação.
- Garantir idempotência por `transaction_id`.
- Persistir o comprovante.
- Publicar o evento `receipt.issued`.

Este serviço não deve:

- Criar transações.
- Debitar conta.
- Creditar conta.
- Confirmar pagamento.
- Reverter pagamento.
- Notificar cliente ou merchant.