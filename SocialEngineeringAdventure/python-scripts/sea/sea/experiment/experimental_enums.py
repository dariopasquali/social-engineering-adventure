from enum import Enum


class LogLevel(Enum):
    INFO = 0
    DEBUG = 1
    ERROR = 2


class DeviceName(Enum):
    MOUSE = 0
    SHIMMER_GSR_PPG = 1
    TOBII = 2
    EYELINK = 3
    ANNOTATIONS = 4
    OPENFACE = 5
