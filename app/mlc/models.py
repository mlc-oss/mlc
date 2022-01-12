"""Models module."""

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.types import Enum
from app.common.mixin import TimeMixin
from app.database import Base
from app.common.status import Status


class Mlc(Base, TimeMixin):
    config_id = Column(Integer, ForeignKey("config.id"))
    zone_name = Column(String(20))
    tenant_id = Column(String(64))  # project id(openstack) or mdq code(cloudstack)
    stack_id = Column(String(64))
    web_port = Column(String(30))
    network_id = Column(String(64))
    public_ip = Column(String(20))
    vrid = Column(Integer)
    status = Column(Enum(Status))
    vip_list = relationship("VIP", back_populates="mlc")
    infra_list = relationship("ServiceInfra", back_populates="mlc")
    config = relationship("Config", backref=backref("mlc", uselist=False))


    def get_status(self):
        return self.status

    def get_id(self):
        return self.id

    def stop(self):
        self.status = Status.STOP

    def start(self):
        self.status = Status.RUNNING

    def get_server(self):
        return [infra for infra in self.infra_list if infra.is_server()][0]

    def get_db(self):
        return [infra for infra in self.infra_list if infra.is_database()][0]

    def get_worker(self):
        return [infra for infra in self.infra_list if infra.is_worker()][0]

    def get_server_vip(self):
        return self.vip_list[0] if self.vip_list[0].is_server() else self.vip_list[1]

    def get_db_vip(self):
        return self.vip_list[0] if self.vip_list[0].is_database() else self.vip_list[1]
