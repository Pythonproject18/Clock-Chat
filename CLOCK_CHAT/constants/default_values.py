from enum import Enum

class Role(Enum):
    ADMIN = 1
    END_USER =2

class Gender(Enum):
    MALE = 1
    FEMALE = 2
    OTHER = 3

class Chat_Type(Enum):
    Personal = 1
    Group = 2
