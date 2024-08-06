from sqlalchemy import Enum


class Status(Enum):
    HTTP_401_UNAUTHORIZED = {
        "code": 401,
        "description": "Could not validate credentials",
        "headers": {"WWW-Authenticate": "Bearer"},
    }
    HTTP_400_BAD_REQUEST = {"code": 400, "description": "Email already registered"}
    HTTP_410_GONE = {"code": 410, "description": "Gone baby gone"}
