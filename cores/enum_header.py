from enum import Enum

class SignalTypeEnum(Enum):
    NPC_DIALOG = 1
    TASK_MARK = 2
    REWARD = 3

class HSVMaskEnum(Enum):
    NORMAL_GREEN_TEXT = 1
    COORDINATE_TEXT = 2
    MOB_DOT = 3
