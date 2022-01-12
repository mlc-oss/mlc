from dependency_injector import containers, providers

from .mlc.services import MlcService
from .mlc.repository import MlcRepository
from .database import Database


# 유저 서비스 , 레포지토리 , DB 클래스 정의

class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    db = providers.Singleton(Database, db_url=config.db.url)
    mlc_repository = providers.Factory(
        MlcRepository,
        session_factory=db.provided.session
    )

    mlc_service = providers.Factory(
        MlcService,
        mlc_repository=mlc_repository,
    )

