from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, validator, BaseConfig, Field
from app.common.status import Status
import re
import json


class SyncResponse(BaseModel):
    message: str = Field(..., example="{job success}" , description="동기 요청에 대한 처리 내용")
    code: str = Field(..., example="200", description="동기 요청에 대한 API status code")
    result: str = Field(..., example=1, description="동기 요청 처리 결과 , 1일경우 성공 2일경우 실패")


class HealthCheckResponse(BaseModel):
    message: str = Field(..., example="Health Check Succeed", description="요청 처리 내용")
    code: str = Field(..., example="200", description="동기 요청에 대한 api status code")
    result: str = Field(..., example=str({"metadatabase_status": "healthy",
                                        "scheduler_status": "healthy",
                                        "latest_scheduler_heartbeat":"string"}), description="헬스체크 응답 결과")


class BaseError(BaseModel):
    message: str

