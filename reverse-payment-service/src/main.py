import os

from configurator import create_app


app = create_app(
    database_path=os.getenv("DATABASE_PATH", "reverse_payment.db"),
    rabbitmq_url=os.getenv("RABBITMQ_URL"),
)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8004, reload=True)
