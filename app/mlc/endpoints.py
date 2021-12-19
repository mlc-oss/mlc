"""Endpoints module."""


from fastapi import APIRouter, Depends,  status,  Header
from fastapi.responses import JSONResponse
from dependency_injector.wiring import inject, Provide
from pydantic import ValidationError
from typing import  Optional

from app.containers import Container
from app.mlc.services import MlcService
from app.common.exception import BatchNotFoundError
from app.dto.param_dto import ParamModel, UpdateModel
from app.dto.message_dto import SyncResponse, HealthCheckResponse, BaseError

router = APIRouter()


@router.get('/mlc/{stack_id}/')
@inject
def get_list(
        batch_id: Optional[int] = None,
        stack_id: str= Header(None),
        tenant_id: str = Header(None),
        mlc_service: MlcService = Depends(Provide[Container.mlc_service]),
):

    if stack_id not in ["G1", "G2"]:
        return JSONResponse(status_code=400, content={"message": "G1 or G2 required"})

    if batch_id:
        return mlc_service.list_batch_by_id(tenant_id=tenant_id, stack_id=stack_id, batch_id= batch_id)

    return mlc_service.list_batch(tenant_id, stack_id)


@router.get('/mlc/start/{stack_id}/{batch_id}/', response_model=SyncResponse)
@inject
def start_service(
        stack_id: str,
        mlc_id: int,
        zone_id: str = Header(None),
        tenant_id: str = Header(None),
        apiKey: str = Header("API-KEY"),
        secretKey: str = Header("SEC_KEY"),
        mlc_service: MlcService = Depends(Provide[Container.mlc_service])
):

    zone = mlc_service.zone_id_to_name(zone_id)
    return mlc_service.start_mlc(tenant_id, stack_id, mlc_id, zone, apiKey, secretKey)


@router.get('/mlc/stop/{stack_id}/{mlc_id}/', response_model=SyncResponse)
@inject
def stop_service(
        mlc_id: int,
        stack_id: str,
        zone_id: str = Header(None),
        tenant_id: str = Header(None),
        apiKey: str = Header("API-KEY"),
        secretKey: str = Header("SEC_KEY"),
        mlc_service: MlcService = Depends(Provide[Container.mlc_service])
):
    zone = mlc_service.zone_id_to_name(zone_id)
    return mlc_service.stop_mlc(tenant_id,stack_id, mlc_id, zone, apiKey, secretKey)


@router.get("/mlc/restart/{stack_id}/{mlc_id}", response_model=SyncResponse)
@inject
def restart_service(
        mlc_id: int,
        stack_id: str,
        zone_id: str = Header(None),
        tenant_id: str = Header(None),
        apiKey: str = Header("API-KEY"),
        secretKey: str = Header("SEC_KEY"),
        mlc_service: MlcService = Depends(Provide[Container.mlc_service])
):
    zone = mlc_service.zone_id_to_name(zone_id)
    return mlc_service.restart_mlc(tenant_id, stack_id,mlc_id, zone, apiKey, secretKey)

@router.post('/mlc/', status_code=status.HTTP_201_CREATED)
@inject
def create_service(
        ParamModel: ParamModel,
        stack_id: str = Header("G1 | G2"),
        tenant_id: str = Header(None),
        zone_id: str = Header(None),
        apiKey: str = Header("API-KEY"),
        secretKey: str = Header("SEC_KEY"),
        mlc_service: MlcService = Depends(Provide[Container.mlc_service]),
):
    
    try:
        parameter = ParamModel
    except ValidationError as e:
        return {"create_service_response": e.errors()}

    if stack_id not in ["aws", "gcp", "azure"]:
        return JSONResponse(status_code=400, content={"message": "not supported csp"})
    return mlc_service.create_mlc(tenant_id, stack_id, parameter.project_name, zone_id, parameter.offering_id, parameter.user_id, parameter.user_pw, parameter.email,
                                      parameter.fname, parameter.lname, parameter.airflowweb_public_port, parameter.kafka_public_port, parameter.maxsize,
                                      parameter.minsize, apiKey, secretKey)


@router.delete('/mlc/{stack_id}/{mlc_id}', status_code=status.HTTP_204_NO_CONTENT)
@inject
def delete_mlc(
        mlc_service: MlcService = Depends(Provide[Container.mlc_service]),
    ):
    return mlc_service.delete_mlc()


@router.put("/mlc/update_config/", response_model=SyncResponse)
@inject
def update_config(
        UpdateModel: UpdateModel,
        zone_id: str = Header(None),
        stack_id: str = Header("G1 | G2"),
        tenant_id: str = Header(None),
        apiKey: str = Header("API-KEY"),
        secretKey: str = Header("SEC_KEY"),
        mlc_service: MlcService = Depends(Provide[Container.mlc_service])
):
    zone = mlc_service.zone_id_to_name(zone_id)
    return mlc_service.update_mlc(tenant_id=tenant_id, stack_id=stack_id,zone=zone, mlc_id=UpdateModel.mlc_id, offering=UpdateModel.offering, api_key=apiKey, sec_key=secretKey)
