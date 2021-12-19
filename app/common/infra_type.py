from enum import Enum


class InfraType(Enum):
    SERVER = "server"
    DATABASE = "database"
    WORKER = "worker"
    NETWORK = "network"
