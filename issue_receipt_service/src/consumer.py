import os
import time

from configurator import create_saga_consumer


def main() -> None:
    rabbitmq_url = os.getenv("RABBITMQ_URL")
    if not rabbitmq_url:
        raise RuntimeError("RABBITMQ_URL is required to start the consumer")

    database_path = os.getenv("DATABASE_PATH", "issue_receipt.db")
    while True:
        try:
            consumer = create_saga_consumer(
                database_path=database_path,
                rabbitmq_url=rabbitmq_url,
            )
            consumer.start()
        except Exception as error:
            print(f"RabbitMQ consumer failed: {error}. Retrying in 5 seconds.")
            time.sleep(5)


if __name__ == "__main__":
    main()
