from enum import Enum, auto

class FieldKey(Enum):
    REMOTE_HOST = auto()
    DATE = auto()
    IDENTITY = auto()
    USERNAME = auto()
    TIME = auto()
    TIMEZONE = auto()
    REQUEST_LINE = auto()
    HTTP_METHOD = auto()
    RESPONSE_SIZE = auto()
    REFERER = auto()
    USER_AGENT = auto()