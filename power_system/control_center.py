from enum import IntEnum


class ControlCenter(IntEnum):
    NDC = 1
    ZAGREB = 2
    RIJEKA = 3
    SPLIT = 4
    OSIJEK = 5
    UNKNOWN = 6

    @classmethod
    def _missing_(cls, value):
        return cls.UNKNOWN
