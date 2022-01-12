from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, validator, BaseConfig, Field
from app.common.status import Status
import re

class ParamModel(BaseModel):
    project_name: str = Field(..., example="mlc-test-project", description="MLC 프로젝트명, 계정별 중복 불가")
    offering_id: str = Field(..., example="1c1v", description="서비스 사양")
    user_id: str = Field(..., example="wonjin", description="최소 8~ 최대 64자리")
    user_pw: str = Field(..., example="seo", description="최소 8~ 최대 64자리")
    email: str = Field(..., example="seowjin1060@naver.com", description="이메일 주소, @ 없을경우 validation error")
    fname: str = Field(..., example="wonjin", description="airflow 정보에 사용될 사용자명(성), ID 아님")
    lname: str = Field(..., example="seo", description="airflow 정보에 사용될 사용자명(이름), ID 아님")
    airflowweb_public_port: str = Field(..., example="9000", description= "1~10999, 12501~65535 사이 포트로 입력")
    kafka_public_port: str = Field(8000, example="8000", description= "1~10999, 12501~65535 사이 포트로 입력")
    maxsize: str = Field(..., example="2" ,description= "최대 5, 최소 1")
    minsize: str = Field(..., example="1", description= "최대 5, 최소 1")
    global zone_list, offering_list, r_email
    zone_list =['KR-CA', 'KR-CB', 'KR-M', 'KR-M2'] # 오퍼링 변경 필요
    offering_list =['1c1v', '2c2v', '4c4v']
    r_email = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')

  #  @validator('zone_name')
  #  def zone_name_must_be_in_list(cls, v):
  #      if v not in zone_list:
  #          raise ValueError('must be selected properly')
  #      return v

#    @validator('offering')
#    def offering_must_be_in_list(cls, v):
#        if v not in offering_list:
#            raise ValueError('must be selected properly')
#        return v

    @validator('email')
    def email_match(cls, v):
        if r_email.match(v) is None:
            raise ValueError('must be formatted correctly')
        return v
    
    @validator('airflowweb_public_port', 'kafka_public_port')
    def valid_port_number(cls, v):
        if not v.isdigit() or int(v)<=0 or int(v)>65535 or 10999<int(v)<12501:
            raise ValueError('must be digit within the scope of 1~10999 or 12501~65535')
        return v
    
    @validator('kafka_public_port')
    def distinct_ports(cls, v, values, **kwargs):
        if 'airflowweb_public_port' not in values.keys() or v == values['airflowweb_public_port']:
            raise ValueError('two port numbers must be distint')
        return v

    @validator('maxsize', 'minsize')
    def maxsize_match(cls, v):
        if not v.isdigit() or not 0<int(v)<6:
            raise ValueError('must more than 0 and less than 6')
        return v

    @validator('minsize')
    def min_less_than_equal_to_max(cls, v, values, **kwargs):
        if 'maxsize' not in values.keys() or v > values['maxsize']:
            raise ValueError('must be less than or equal to maxsize')
        return v


class UpdateModel(BaseModel):
    batch_id: int =Field(..., example="")
    offering: str = Field(..., example="")



