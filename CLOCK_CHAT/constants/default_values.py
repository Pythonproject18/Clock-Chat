from enum import Enum

class Role(Enum):
    ADMIN = 1
    END_USER =2

class Gender(Enum):
    MALE = 1
    FEMALE = 2
    OTHER = 3

class ResponseMessageType(Enum):
    SUCCESS='success'
    ERROR='error'
    WARNING='warning'
    INFO='info'
    NONE='null'

class Status_Type(Enum):
    IMAGE = 1
    VIDEO = 2
    TEXT = 3