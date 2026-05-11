import logging
import os
import time

from observability.logging import configure_logging

from configurator import create_debit_completed_consumer


logger = logging.getLogger(__name__)


def main() -> None:
    configure_logging()
    rabbitmq_url = os.getenv("RABBITMQ_URL")
    if not rabbitmq_url:
        raise RuntimeError("RABBITMQ_URL is required to start the consumer")

    database_path = os.getenv("DATABASE_PATH", "credit_account.db")
    while True:
        try:
            consumer = create_debit_completed_consumer(
                database_path=database_path,
                rabbitmq_url=rabbitmq_url,
            )
            consumer.start()
        except Exception:
            logger.exception("rabbitmq consumer failed; retrying in 5 seconds")
            time.sleep(5)


if __name__ == "__main__":
    main()
