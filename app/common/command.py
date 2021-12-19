from enum import Enum


class Command(Enum):
    LIST = "Batch_List"
    CREATE = "Batch_Create"
    DELETE = "Batch_Delete"
    UPDATE = "Batch_Update"
    RUN = "Batch_Run"
    STOP = "Batch_Stop"
    RESTART = "Batch_Restart"
