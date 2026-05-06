# guess_ship_name.py（猜船名任务文件）
import random

from azurlane.name import ship_name_map

from base.base_task import BaseTask
from constants.command_constants import CommandType
from constants.multi_task_constants import TaskType, MultiRoundTaskStatus


class GuessShipNameTask(BaseTask):
    """猜船名任务类"""
    SHIP_MAP = ship_name_map

    def __init__(self):
        super().__init__(TaskType.GuessShipName)  # 记得在 TaskType 加这个
        self.task_status = MultiRoundTaskStatus.INIT

        # 游戏统计
        self.total_round = 0
        self.correct_count = 0
        self.wrong_count = 0

        # 当前题目
        self.current_code = None
        self.current_answer = None

    def reset(self):
        """重置游戏状态"""
        self.total_round = 0
        self.correct_count = 0
        self.wrong_count = 0
        self.current_code = None
        self.current_answer = None
        self.task_status = MultiRoundTaskStatus.INIT

    def end(self):
        """结束任务"""
        self.task_status = MultiRoundTaskStatus.END

    def _generate_new_question(self):
        """随机生成新题目"""
        self.current_code = random.choice(list(self.SHIP_MAP.keys()))
        self.current_answer = self.SHIP_MAP[self.current_code]

    def play_round(self, user_input: str) -> dict:
        user_answer = user_input.strip()

        # 还没出题 → 先出题
        if self.current_code is None:
            self._generate_new_question()
            self.total_round += 1
            self.task_status = MultiRoundTaskStatus.PLAYING
            return {
                "success": True,
                "msg": f"【题目】请说出这个代号对应的舰名：\n【{self.current_code}】",
                "round": self.total_round
            }

        # 已有题目 → 判断答案
        correct_answer = self.current_answer
        is_correct = user_answer == correct_answer

        if is_correct:
            self.correct_count += 1
            result_msg = "✅ 回答正确！"
        else:
            self.wrong_count += 1
            result_msg = f"❌ 回答错误！正确答案是：【{correct_answer}】"

        # 答完立刻生成下一题
        self._generate_new_question()
        self.total_round += 1

        return {
            "success": True,
            "msg": (
                f"{result_msg}\n\n"
                f"【下一题】\n代号：【{self.current_code}】"
            ),
            "total_round": self.total_round,
            "correct": self.correct_count,
            "wrong": self.wrong_count
        }

    def handle_command(self, msg_content: str) -> dict:
        """处理用户输入"""
        return self.play_round(msg_content)

    def get_valid_cmds(self):
        return True

    def get_summary(self) -> str:
        """任务总结"""
        return (
            f"共答题 {self.total_round} 轮\n"
            f"✅ 正确：{self.correct_count} 次\n"
            f"❌ 错误：{self.wrong_count} 次"
        )

    def get_prompt(self, param, **kwargs):
        """提示文本"""
        match param:
            case CommandType.MULT_BASE_START.value:
                return "🚢 猜舰名游戏开始！\n我会给你一个代号，请说出对应的舰名。\n 输入【开始】开始答题"
            case CommandType.MULT_BASE_END.value:
                return f"游戏结束！\n{self.get_summary()}"
            case CommandType.MULT_BASE_TIMEOUT.value:
                return f"游戏超时结束！\n{self.get_summary()}"
            case CommandType.MULT_BASE_INVALID_CMD.value:
                return "⚠️ 输入无效，请直接回答舰名！"
            case _:
                return f"未知提示：{param}"
