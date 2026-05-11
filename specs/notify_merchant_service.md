# Notify Merchant Service

## Descrição de Negócio

O `notify_merchant_service` é responsável por notificar o recebedor após uma transação de pagamento ser confirmada.

Este serviço pertence ao contexto de Notificação e representa a etapa de comunicação com o merchant/lojista na saga de pagamento.

Ele consome o evento `payment.confirmed`, cria uma notificação para o merchant, tenta realizar a entrega pelo canal configurado e publica o evento `merchant.notified`.

## Bounded Context

Notificação.

## Ubiquitous Language

- Notification: mensagem enviada para um destinatário.
- NotificationId: identificador único da notificação.
- Merchant: recebedor do pagamento.
- Recipient: destinatário da notificação.
- Channel: canal de entrega da notificação.
- DeliveryStatus: estado atual da entrega.
- PaymentConfirmed: evento que informa que o pagamento foi confirmado.

## Aggregate Root

### Notification

A `Notification` é o Aggregate Root do contexto de Notificação.

Ela controla o ciclo de vida da notificação e garante que a entrega seja registrada corretamente.

## Estados da Notificação

- PENDING
- DELIVERED
- FAILED

## Invariantes

- O merchant só pode ser notificado após o pagamento ser confirmado.
- Uma notificação deve possuir um destinatário válido.
- Uma notificação deve possuir um canal válido.
- Uma notificação deve estar associada a um `transaction_id`.
- O mesmo merchant não deve receber notificações duplicadas para a mesma transação.
- A operação deve ser idempotente por `transaction_id` e `merchant_id`.
- Falha na notificação não deve reverter ou cancelar o pagamento.

## Caso de Uso Principal

### NotifyMerchant

Responsável por notificar o merchant após o pagamento ser confirmado.

Entrada esperada:

- transaction_id
- customer_id
- merchant_id
- amount
- confirmed_at

Saída esperada:

- notification_id
- transaction_id
- merchant_id
- status
- notified_at

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

### MerchantNotified

Publicado quando a notificação do merchant é processada com sucesso.

Payload sugerido:

- notification_id
- transaction_id
- merchant_id
- amount
- channel
- status
- notified_at

## Portas

### NotificationRepository

Responsável por salvar e recuperar notificações.

### NotificationGateway

Responsável por entregar a notificação por um canal externo.

### EventPublisher

Responsável por publicar eventos de domínio.

## Responsabilidades

Este serviço deve:

- Consumir o evento `payment.confirmed`.
- Criar uma notificação para o merchant.
- Validar o destinatário.
- Validar o canal de entrega.
- Tentar entregar a notificação.
- Persistir o resultado da notificação.
- Publicar o evento `merchant.notified`.

Este serviço não deve:

- Criar transações.
- Debitar conta.
- Creditar conta.
- Confirmar pagamento.
- Reverter pagamento.
- Notificar cliente.
- Emitir comprovante.