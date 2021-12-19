from enum import Enum


class ResponseType(Enum):
    JSON = "json"
    XML = "xml"

class response():
    def __init__(self ):
        pass
    def create_response(self, endpoint: str, parameters: dict, response_type :ResponseType):
        if response_type.value == "json":
            response = {}
            response[endpoint+"response"] = parameters


        elif response_type.value == "xml":
            #response = {}
            response = {}

        return response
