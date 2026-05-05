# rock_paper_scissors.py（猜拳任务文件）
import random

from base.base_task import BaseTask
from constants.command_constants import CommandType
from constants.multi_task_constants import TaskType, RockPaperScissors


class RockPaperScissorsTask(BaseTask):
    """猜拳游戏任务类"""
    CHOICES = ["石头", "剪刀", "布"]
    WIN_RULES = {"石头": "剪刀", "剪刀": "布", "布": "石头"}

    # 多格式指令映射表：所有格式 → 标准中文
    FORMAT_MAP = {
        # 中文格式
        "石头": "石头", "剪刀": "剪刀", "布": "布",
        # 英文格式（大小写通用）
        "rock": "石头", "Rock": "石头", "ROCK": "石头",
        "scissors": "剪刀", "Scissors": "剪刀", "SCISSORS": "剪刀",
        "paper": "布", "Paper": "布", "PAPER": "布",
        # Emoji格式
        "✊": "石头", "✊️": "石头",
        "✌️": "剪刀", "✌": "剪刀", "✂️": "剪刀",
        "✋": "布", "✋️": "布"
    }

    def normalize_choice(self, user_input):
        """
        标准化用户输入：自动识别中文/英文/emoji，返回标准中文指令
        :param user_input: 用户输入的任意格式指令
        :return: 标准中文指令 / None（无效输入）
        """
        return self.FORMAT_MAP.get(user_input.strip())

    def __init__(self):
        super().__init__(TaskType.RockPaperScissors)
        self.round_num = 0  # 当前轮数
        self.user_win = 0  # 用户赢的次数
        self.bot_win = 0  # 机器人赢的次数
        self.draw_num = 0  # 平局次数
        self.last_user_choice = None
        self.last_bot_choice = None
        self.task_status = RockPaperScissors.INIT

    def reset(self):
        """重置猜拳游戏"""
        self.round_num = 0
        self.user_win = 0
        self.bot_win = 0
        self.draw_num = 0
        self.last_user_choice = None
        self.last_bot_choice = None
        self.task_status = RockPaperScissors.INIT

    def end(self):
        """结束猜拳游戏"""
        self.task_status = RockPaperScissors.END

    def play_round(self, user_input: str) -> dict:
        """单轮猜拳逻辑"""
        user_choice = self.normalize_choice(user_input)
        if user_choice not in self.CHOICES:
            return {"success": False, "msg": f"输入错误！请选择：{','.join(self.CHOICES)}"}

        bot_choice = random.choice(self.CHOICES)
        self.round_num += 1
        self.last_user_choice = user_choice
        self.last_bot_choice = bot_choice

        if user_choice == bot_choice:
            self.draw_num += 1
            result = "平局"
        elif self.WIN_RULES[user_choice] == bot_choice:
            self.user_win += 1
            result = "你赢了"
        else:
            self.bot_win += 1
            result = "我赢了"

        self.task_status = RockPaperScissors.PLAYING
        return {
            "success": True,
            "msg": f"你出了{user_choice}，我出了{bot_choice} → {result}！",
            "round_num": self.round_num,
            "user_win": self.user_win,
            "bot_win": self.bot_win,
            "draw_num": self.draw_num
        }

    def get_valid_cmds(self):
        return self.CHOICES

    def get_summary(self) -> str:
        """汇总游戏结果"""
        total = self.user_win + self.bot_win + self.draw_num
        return f"共玩{total}轮 → 你赢{self.user_win}轮，我赢{self.bot_win}轮，平局{self.draw_num}轮～"

    def get_prompt(self, param, **kwargs):
        match param:
            case CommandType.MULT_BASE_START.value:
                return f"开始猜拳游戏！请输入：{','.join(self.CHOICES)}"
            case CommandType.MULT_BASE_END.value:
                return f"游戏结束！{self.get_summary()}"
            case CommandType.MULT_BASE_TIMEOUT.value:
                return f"游戏已结束！{self.get_summary()}"
            case CommandType.MULT_BASE_INVALID_CMD.value:
                return f"输入错误！请输入：{','.join(self.CHOICES)}"
            case _:
                return f"未知提示类型：{param}"
