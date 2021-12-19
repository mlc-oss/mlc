from typing import Optional

class BaseError(Exception):
    code: str
    message: str
    
    def __init__(self, code: int, message: str) -> None:
        self.code = code
        self.message = message


class InfraCreationError(BaseError):
    infra_type: str
    infra_id: str
    jobid_exist: bool

    def __init__(self, code: int, message: str,
                       infra_type: str,jobid_exist: bool, infra_id: str = None) -> str:
        super().__init__(code, message)
        self.infra_type = infra_type
        self.jobid_exist = jobid_exist
        self.infra_id = infra_id
    
    def __str__(self) -> str:
        rst = f'{self.code}: {self.message} \
               \nError occurred during deploying {self.infra_type} \
               \nJob ID exist: {self.jobid_exist}'
        return rst

class AnsibleError(BaseError):
    task_type: str

    def __init__(self, code: int, message: str,
                 task_type: str) -> None:
        super().__init__(code, message)
        self.task_type = task_type

    def __str__(self) -> str:
        rst = f'{self.code}: {self.message} \
               \nError occurred during ansible task execute  {self.task_type}'
        return rst