from pydantic import BaseModel


class AnsibleHost(BaseModel):
    zone : str
    name : str
    ansible_connection: str
    ansible_ip: str
    ansible_port: str
    ansible_ssh_pass: str
    infra_type: str
    tenant_id: str
    is_master: str
    script_parameters: dict


class AnsibleTemplate(BaseModel):
    name: str
    tenant_id: str
    batch_id: str


class AnsibleInventory(BaseModel):
    tenant_id: str
    zone: str


class AnsibleProject(BaseModel):
    type: str
    infra: str


