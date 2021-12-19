"""Services module."""

import json
import requests
from requests.auth import HTTPBasicAuth
from app.ansible.variables import AnsibleTemplate,AnsibleHost , AnsibleInventory
from app.dto.error_dto import AnsibleError
import json


class Session:
    def get_token(self):
        url = "http://10.213.194.98/api/v2/tokens"
        payload = {}
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Basic '
        }
        response = requests.request("GET", url, verify=False, headers=headers, data=payload,
                                    auth=HTTPBasicAuth('admin', 'password'))


class AnsibleService(Session):
    def __init__(self) -> None:
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Basic '
        }
        self.ansible_id = "admin"
        self.ansible_pw = "password"
        self.url = "http://10.213.194.98/api/v2/"

    def get_inventory(self, tenant_id):
        url = self.url+"inventories/?search={}".format(tenant_id)
        payload = {}
        files = {}
        headers = self.headers
        inventory_id = ''
        response = requests.request("GET", url, headers=headers, data=payload, files=files,
                                     auth=HTTPBasicAuth(self.ansible_id, self.ansible_pw))
        response = json.loads(response.text)
        api_result = response['results'][0]
        inventory_id = api_result['id']
        return inventory_id

    def get_organization(self, zone):
        url = self.url+"organizations/"
        payload = {}
        files = {}
        headers = self.headers
        response = requests.request("GET", url, headers=headers, data=payload, files=files,
                                    auth=HTTPBasicAuth(self.ansible_id, self.ansible_pw))
        response = json.loads(response.text)
        for organization in response['results']:
            if organization["name"] == zone:
                organization_id = organization['id']
                return organization_id
        raise AnsibleError(code=500, message="Not available zone ", task_type="create_template")

    def get_template_id(self, name):
        url = "http://10.213.194.98/api/v2/job_templates/?search={}".format(name)
        payload = {}
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Basic'
        }
        response = requests.get(url, verify=False,data=payload, headers=headers,
                                auth=HTTPBasicAuth('admin', 'password'))
        json_response = json.loads(response.text)

        if json_response:
            api_result = json_response['results'][0]
            template_id = api_result['id']
            return template_id
        else:
            raise AnsibleError(code=500, message="get template error", task_type="create_template")

    def check_job_status(self, job_id):
        url = self.url + '/api/v2/jobs/{id}/'.format(id=job_id)
        headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + self.ansible_pw}

        req = requests.request(url, None, headers)

        while True:
            response = requests.urlopen(req)
            json_data = json.loads(response.read())

            print("job status : {status}".format(status=json_data.get('status')))

            if json_data.get('status') == 'successful':
                return True
            else:
                return False

    def create_inventory(self, inventory:AnsibleInventory):
        organization_id = self.get_organization(inventory.zone)
        url = self.url+"inventories/"
        payload = json.dumps({
            "name": inventory.tenant_id,
            "organization": organization_id
        })
        headers = self.headers
        inventory_id = ''
        response = requests.request("POST", url, headers=headers, data=payload,
                                    auth=HTTPBasicAuth(self.ansible_id, self.ansible_pw))
        print(f"create_inventory request {response.request.url } {response.request.body}")

        return inventory_id


    def create_host(self, host: AnsibleHost):
        inventory_id = self.get_inventory(tenant_id=host.tenant_id)
        url = self.url + "inventories/{}/hosts/".format(inventory_id)
        variables = {
            "description": "auto input host from ktcloud",
            "ansible_ssh_port": host.ansible_port,
            "ansible_connection": "ssh",
            "ansible_host": host.ansible_ip,
            "ansible_ssh_pass": host.ansible_ssh_pass,
            "infra_type": host.infra_type,
            "tenant_id": host.tenant_id,
            "is_master": host.is_master,
            "is_installed": "0"}

        for key in host.script_parameters.keys():
            variables[key] = host.script_parameters[key]

        data = {
            "name": host.name,
            "variables": str(variables)
        }


        payload = json.dumps(data)
        headers = self.headers
        response = requests.request("POST", url, headers=headers, data=payload,
                                    auth=HTTPBasicAuth(self.ansible_id, self.ansible_pw))
        print(f"create_host request {response.request.url}")
        print(f"create_host request {response.request.body}")

        return response

    def create_template(self, template: AnsibleTemplate):
        inventory_id = self.get_inventory(template.tenant_id)
        url = self.url + "job_templates/"
        payload = json.dumps({
            "name": template.name,
            "description": "run request from {}".format(template.tenant_id),
            "project": 10,
            "playbook": "service_init.yml",
            "job_type": "run",
            "inventory": inventory_id
        })
        headers = self.headers
        response = requests.request("POST", url, headers=headers, data=payload,
                                    auth=HTTPBasicAuth(self.ansible_id, self.ansible_pw))
        print(f"create_template request {response.request.url} {response.request.body}")
        print(response)
        return response

    def run_template(self, name: str):
        template_id = self.get_template_id(name)
        url = self.url + "job_templates/{}/launch/".format(template_id)

        payload = json.dumps({
            "description": "auto input host from ktcloud",
            "project": 2,
            "playbook": "service_init.yml",
            "job_type": "run",
        })

        headers = self.headers
        response = requests.request("POST", url, headers=headers, data=payload,
                                    auth=HTTPBasicAuth(self.ansible_id, self.ansible_pw))
        print(f"create_template request {response.request.url} {response.request.body}")
        print(response)
        print(response)
        return response

    def get_host_all(self, host_name: list):
        res = []
        headers = self.headers
        for name in host_name:
            print(name)
            url = self.url + "hosts/?search={}".format(name)
            print(url)
            response = requests.request("GET", url, headers=headers,
                                        auth=HTTPBasicAuth(self.ansible_id, self.ansible_pw))
            response = json.loads(response.text)
            api_result = response['results']
            print(response)
            for host in api_result:
                res.append(host['id'])
        return res

    def delete_host(self, host_id: list):
        url = self.url + "hosts/"
        payload = {}
        headers = self.headers
        for id in host_id:
            request_url = url + str(id)
            print(url)
            response = requests.delete(url=request_url, headers=headers, data=payload,
                                       auth=HTTPBasicAuth(self.ansible_id, self.ansible_pw))
            print(response)
        return response

    def template_status(self, template):
        template_id = self.get_template_id()
