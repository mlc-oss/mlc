
from sqlalchemy import Column, String,  Integer, ForeignKey
from sqlalchemy.types import Enum
from sqlalchemy.orm import relationship
from app.common.mixin import TimeMixin
from app.database import Base
from app.common.infra_type import InfraType


class ServiceInfra(Base, TimeMixin):
    batch_id = Column(Integer, ForeignKey("mlc.id"))
    master_id = Column(String(64))
    slave_id = Column(String(64))
    master_ip = Column(String(20))
    slave_ip = Column(String(20))
    group_name = Column(String(64))
    infra_type = Column(Enum(InfraType))

    batch = relationship("Batch", back_populates="infra_list")

    def is_server(self):
        return self.infra_type == InfraType.SERVER

    def is_database(self):
        return self.infra_type == InfraType.DATABASE

    def is_worker(self):
        return self.infra_type == InfraType.WORKER
