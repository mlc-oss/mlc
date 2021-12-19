from enum import Enum


class Status(Enum):
    RUNNING = 'running'
    STOP = 'stop'
    DELETED = 'deleted'
    ERROR = 'error'
    CREATE = 'creating'
    DELETE = 'deleting'
    RESTART = 'restarting'
    STOPPING = 'stopping'
    START = 'starting'
    UPDATE = 'updating'
    DELETEERROR = "delete error"
    CREATEERROR = "create error"
    # stopping
    # deleting
    # restarting
    # 동작
    ## 생성중인 상태 추가
    ##
class JobStatus(Enum):
    PENDING = 0
    SUCCESS = 1
    FAIL = 2
