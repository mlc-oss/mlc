from app.common.infra_type import InfraType


class NotFoundError(Exception):
    entity_name: str
    def __init__(self, entity_id):
        super().__init__(f'{self.entity_name} not found, id: {entity_id}')


class InvalidTypeError(Exception):
    def __init__(self, infra_type: InfraType):
        super().__init__()


class InvalidStatusError(Exception):
    def __init__(self, infra_type: InfraType ):
        super().__init__()


class BatchNotFoundError(NotFoundError):
    entity_name: str = 'Batch'
    def __init__(self, entity_id):
        super().__init__(entity_id)