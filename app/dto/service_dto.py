from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from app.common.status import Status

class MlcBase(BaseModel):
    id: int = Field(..., description="고객 Mlc 서비스 ID")
    public_ip: str = Field(..., description="Mlc 서비스 public IP")
    public_port: str = Field(..., description="Mlc 서비스 Airflow 콘솔 접속 포트")
    offering: str = Field(..., description="구성 스케줄러 사양")
    project_name: str = Field(..., description="Mlc 서비스 프로젝트명")
    date: Optional[datetime] = None
    status: Status = Field(..., description="서비스 상태, Created , Deleted , Error, Stop")
    zone_id: str = None
    worker_max: str = None
    worker_min: str = None

class MlcList(BaseModel):
    message: str
    batch: List[MlcBase] = []


class NetWork(BaseModel):
    public_ip: Optional[str] = None
    airflowweb_public_port: Optional[str] = None
    rabbitmqweb_public_port: Optional[str] = None


class VipList(BaseModel):
    server_vip: Optional[str] = None
    db_vip: Optional[str] = None


class InfraList(BaseModel):
    server_master_id: Optional[str] = None
    server_slave_id: Optional[str] = None
    db_master_id: Optional[str] = None
    db_slave_id: Optional[str] = None
    autoscalinggroupname: Optional[str] = None


class MlcInfra(BaseModel):
    batchid: str
    network: Optional[List[NetWork]] = ['']
    vip_list: Optional[List[VipList]] = ['']
    infra_list: Optional[List[InfraList]] = ['']
    zoneid: str


class MlcWithInfra(BaseModel):
    Mlc : MlcBase
    batch_infra: MlcInfra


class BatchDelete(BaseModel):
    message: str
    batch: List[MlcBase] = []


class BatchStatus(BaseModel):
    batch_id: int
    status: Status
