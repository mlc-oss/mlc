"""Services module."""
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from celery import chord

from .models import Mlc
from .repository import MlcRepository
from app.service_infra.models import ServiceInfra
from app.dto.service_dto import MlcList, MlcBase, NetWork, MlcInfra, VipList, InfraList,  MlcWithInfra
from app.common.infra_type import InfraType
from app.common.status import Status, JobStatus
from app.module import mlc
from app.dto.error_dto import  InfraCreationError, AnsibleError
from app.dto.message_dto import SyncResponse
from json.decoder import JSONDecodeError
from app.ansible.services import AnsibleService
from app.ansible.variables import AnsibleInventory, AnsibleTemplate

class MlcService:
    def __init__(self, mlc_repository: MlcRepository) -> None:
        self._mlc_repository:  MlcRepository = mlc_repository

    ## 모든 서비스 config값을 읽어서 중복 프로젝트명 확인
    def check_project_name(self, tenant_id, project_name):
        mlc_list = self._mlc_repository.find_all_with_infra(tenant_id=tenant_id)
        if mlc_list is None:
            return False
        for mlc in mlc_list:
            if mlc.config == None:
                continue

            if mlc.config.project_name == project_name:
                return True
        return False

    def list_mlc_service(self, tenant_id: str, stack_id: str):
        mlc_list = self._mlc_repository.find_all_with_stack_id(tenant_id, stack_id)
        mlc_bases = []
        for mlc in mlc_list:
            mlc_bases.append(
                MlcBase(id=mlc.id
                          , public_ip=mlc.public_ip
                          , public_port= mlc.web_port
                          , offering=mlc.config.offering
                          , project_name=mlc.config.project_name
                          , date=mlc.created_at
                          , status=mlc.status
                          , zone_id=mlc.config.zone_id
                          , worker_max = mlc.config.worker_max
                          , worker_min = mlc.config.worker_min
                          )
            )

        return MlcList(message="listAll", mlc=mlc_bases)

    def list_mlc_by_id(self, tenant_id: str, stack_id: str, mlc_id: int) -> Mlc:
        if self.__verify_accessible(tenant_id, mlc_id):
            result = self._mlc_repository.find_by_id_with_stack_id(tenant_id, stack_id, mlc_id)
            if result.status == Status.CREATE or result.status ==Status.CREATEERROR:
                return MlcBase(
                                    id=result.id
                                    , public_ip=result.public_ip
                                    , public_port=result.web_port
                                    , offering=result.config.offering
                                    , project_name=result.config.project_name
                                    , date=result.created_at
                                    , status=result.status
                                    , zone_id=result.config.zone_id
                                    , worker_max = result.config.worker_max
                                    , worker_min=result.config.worker_min)
                #return JSONResponse(status_code=400, content={"message": "mlc deployment in pending please wait until deployment finished for infra info"})

            return MlcWithInfra(message="listById"
                                                , mlc=MlcBase(id=result.id
                                                , public_ip=result.public_ip
                                                , public_port=result.web_port
                                                , offering=result.config.offering
                                                , project_name=result.config.project_name
                                                , date=result.created_at
                                                , status=result.status
                                                , zone_id=result.config.zone_id
                                                , worker_max = result.config.worker_max
                                                , worker_min=result.config.worker_min
                                                ),
                                mlc_infra=MlcInfra(mlcid=result.get_id()
                              , network=[NetWork(public_ip=result.public_ip,
                                                 airflowweb_public_port=result.web_port,
                                                 rabbitmqweb_public_port="5672")]
                              , vip_list=[VipList(server_vip=result.get_server_vip().private_ip,
                                                  db_vip=result.get_db_vip().private_ip)]
                              , infra_list=[InfraList(server_master_id=result.get_server().master_id,
                                                      server_slave_id=result.get_server().slave_id,
                                                      db_master_id=result.get_db().master_id,
                                                      db_slave_id=result.get_db().slave_id,
                                                      autoscalinggroupname=result.get_worker().group_name
                                                      )]
                              , zoneid=result.zone_name)
                             )
        else:
            return JSONResponse(status_code=404, content={"message": "requested mlc not found"})

    def create_mlc(self, tenant_id: str, stack_id: str, project_name: str, zone_id: str, offering: str, user_id: str, user_pw: str, email: str,
                     fname: str, lname: str, airflowweb_public_port: str, kafka_public_port: str, maxsize: str,
                     minsize: str, api_key: str , sec_key: str):
        ansible = AnsibleService()
        zone_name = self.zone_id_to_name(zone_id)
        ansible.create_inventory(inventory=AnsibleInventory(tenant_id=tenant_id, zone=zone_name))
        # delegate task to celery
        from app.containers import Container
        mlc_repository = Container.mlc_repository()

        try:
            self.deploy_k8s.delay()
            #self.deploy_kafka.delay()
            #self.deploy_airflow.delay()
            #self.deploy_ml.delay()

        except Exception as e:
            mlc_repository.find_by_id_with_stack_id(tenant_id, stack_id)
            mlc.status = Status.CREATEERROR
            mlc_id = mlc_repository.update(mlc)
            return JSONResponse(status_code=500,
                                content={"message": "mlc service creation request failed"})
        return "성공시 응답"

    @mlc.task(bind=True)
    def deploy_kafka(self, job_uuid: str, tenant_id: str, stack_id: str, project_name: str, zone_id: str, offering: str, vrid: str, user_id: str, user_pw: str,
                     email: str, fname: str, lname: str, airflowweb_public_port: str, rabbitmq_public_port: str,
                     maxsize: str, minsize: str, api_key: str, sec_key: str, mlc_id: str):
        try:
            print('deploy kafka logic')

        except (InfraCreationError, AnsibleError) as e:
            return (e.__str__())
        except JSONDecodeError as e:
            return (e.__str__())
        except Exception as e:
            import Container
            print("handling exception",e)
            mlc_repository = Container.mlc_repository()
            mlc.status = Status.CREATEERROR
            mlc_id = mlc_repository.update(mlc)
            return (e.__str__())

    def delete_mlc(self, tenant_id: str, stack_id, batch_id , api_key, sec_key):
        return

    # failover
    def start_mlc(self, tenant_id: str, stack_id:str , batch_id: int, zone:str, api_key , sec_key):
        return

    def stop_mlc(self, tenant_id: str, stack_id:str , batch_id: int, zone:str, api_key , sec_key):
        try:
            self.stop_service.delay(tenant_id, stack_id,batch_id, zone, api_key, sec_key)
        except Exception as e:
            return e.__str__()
        return SyncResponse(code="200", message="stop requested mlc service", result=1)

    def restart_mlc(self, tenant_id: str, stack_id:str , batch_id: int, zone:str, api_key , sec_key):
        pass

    def update_mlc(self, tenant_id: str, stack_id: str, batch_id: int, offering:str, zone: str, api_key, sec_key):
        return SyncResponse(code="200", message="update requested mlc service", result=1)
