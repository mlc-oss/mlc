"""Application module."""

from fastapi import FastAPI
from app.containers import Container
from app.mlc import endpoints as mlc_endpoints
from os import path, environ

base_dir = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))


def create_app() -> FastAPI:
    container = Container()
  #  container.config.from_yaml('config.yml')
    container.wire(modules=[mlc_endpoints])
    db = container.db()
    db.init_database()
    app = FastAPI(BASE_DIR=base_dir)
    app.container = container
    app.include_router(mlc_endpoints.router)
    return app


app = create_app()
