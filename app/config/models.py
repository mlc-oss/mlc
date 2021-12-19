from sqlalchemy import Column, String

from app.common.mixin import TimeMixin
from app.database import Base


class Config(Base, TimeMixin):
    project_name = Column(String(64))
    airflow_id = Column(String(64))
    airflow_pw = Column(String(64))
    email = Column(String(64))
    first_name = Column(String(32))
    last_name = Column(String(32))
    zone_id = Column(String(64))
    worker_group_name = Column(String(64))
    worker_max = Column(String(32))
    worker_min = Column(String(32))
    offering = Column(String(64))

    @classmethod
    def create_config(cls, config: dict):
        config = Config(project_name=config["project_name"],
                        airflow_id=config["airflow_id"],
                        airflow_pw=config["airflow_pw"],
                        email=config["email"]
                        )
        return config

    def update_config(self):
        pass
