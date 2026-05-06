# multi_task_constants.py（多轮任务 枚举/常量文件）
from enum import Enum

class SessionStatus(Enum):
    """用户会话全局状态"""
    IDLE = "idle"          # 闲置
    ACTIVE = "active"      # 活跃
    TIMEOUT = "timeout"    # 超时
    FINISHED = "finished"  # 完成
class TaskType(Enum):
    """任务类型标识"""
    RockPaperScissors = "rock_paper_scissors"  # 猜拳游戏
    GuessShipName = "guess_ship_name" # 猜舰名


class MultiRoundTaskStatus(Enum):
    """多轮任务状态"""
    INIT = "init"        # 初始化
    PLAYING = "playing"  # 进行中
    END = "end"          # 结束

class RockPaperScissors(Enum):
    """猜拳任务专属状态"""

class GuessShipNameStatus(Enum):
    """猜船名任务专属状态"""