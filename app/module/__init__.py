from celery import Celery

mlc = Celery("Mlc", broker="amqp://guest:guest@rabbitmq:5672", backend="db+postgresql+psycopg2://admin:admin@postgres:5432/mlc")
