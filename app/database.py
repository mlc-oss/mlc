"""Database module."""

from contextlib import contextmanager
import logging
from contextlib import contextmanager, AbstractContextManager
from sqlalchemy import create_engine, orm
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from typing import Callable

logger = logging.getLogger(__name__)
Base = declarative_base()
pool_recycle = 900


class Database:
    def __init__(self, db_url: str) -> None:
        # production database(depreciated)
        '''
        self._engine = create_engine("mysql+pymysql://airflow_webserver:seo1060@211.252.84.114:35000/airflow_webserver"
            , echo=True,pool_recycle= pool_recycle,
            pool_pre_ping=True)


        self._engine = create_engine("sqlite:///./sql_app.db"
                                     , connect_args={"check_same_thread": False}, echo=True)
        '''
        self._engine = create_engine('postgresql+psycopg2://admin:admin@postgres:5432/ktcloud',
                                     # , connect_args={"check_same_thread": False},
                                     pool_pre_ping=True,
                                     pool_use_lifo=True,
                                    echo=True)

        self._session_factory = orm.scoped_session(
            orm.sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self._engine,
            ),
        )

    def init_database(self) -> None:

        from app.mlc.models import Mlc
        from app.config.models import Config
        from app.service_infra.models import ServiceInfra

        ## pymysql 이슈로 인해 커넥터 변경중, pymysql에서 의존성 주입으로 인한 다중 쿼리 처리 불가
        Base.metadata.create_all(self._engine)

        # @app.on_event("startup")
        # def startup():
        #    self._engine.connect()
        #    logging.info("DB connected.")

        # @app.on_event("shutdown")
        # def shutdown():
        #    self._session.close_all()
        #    self._engine.dispose()
        #    logging.info("DB disconnected")
        pass

    @contextmanager
    def session(self):
        session: Session = self._session_factory()
        try:
            yield session
        except Exception:
            logger.exception('Session rollback because of exception')
            session.rollback()
            raise
        finally:
            session.close()

    @property
    def session_factory(self):
        return self._session_factory
