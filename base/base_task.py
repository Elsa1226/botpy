# base_task.py（任务基类文件）

# base_task.py
from constants.command_constants import (
    MULTI_ROUND_DEFAULT_TEMPLATES,
    MULTI_ROUND_TASK_TEMPLATES,
    MULTI_ROUND_VALID_CMDS
)
from constants.multi_task_constants import TaskType

class BaseTask:
    """任务基类：定义通用接口+文本获取逻辑"""
    def __init__(self, task_type: TaskType):
        self.task_type = task_type  # 任务类型
        self.task_status = None     # 任务内状态
        # 任务名称
        self.task_name = self._get_task_name()
        # 任务专属模板（无则用通用）
        self.task_templates = MULTI_ROUND_TASK_TEMPLATES.get(self.task_type.value, {})

    def _get_task_name(self) -> str:
        """获取任务名称"""
        name_map = {
            TaskType.RockPaperScissors.value: "猜拳游戏",
        }
        return name_map.get(self.task_type.value, "未知任务")

    def get_prompt(self, prompt_type: str, **kwargs) -> str:
        """
        获取任务文本提示
        :param prompt_type: 提示类型（start/end/timeout/invalid_cmd）
        :param kwargs: 动态参数（如round_num/user_win）
        :return: 格式化后的提示文本
        """
        # 优先用任务专属模板，无则用通用模板
        template = self.task_templates.get(prompt_type, MULTI_ROUND_DEFAULT_TEMPLATES[prompt_type])
        # 补充默认参数（task_name/valid_cmds）
        kwargs.setdefault("task_name", self.task_name)
        kwargs.setdefault("valid_cmds", MULTI_ROUND_VALID_CMDS.get(self.task_type.value, ""))
        # 格式化模板
        return template.format(** kwargs)

    def handle_command(self, msg_content: str) -> str:
        """处理用户指令"""
        raise NotImplementedError("子类必须实现handle_command方法")

    def get_valid_cmds(self) -> list | bool:
        """获取当前任务的合法指令"""
        raise NotImplementedError("子类必须实现get_valid_cmds方法")

    def get_summary(self) -> str:
        """获取任务总结"""
        raise NotImplementedError("子类必须实现get_summary方法")

    def reset(self):
        """重置任务状态"""
        raise NotImplementedError("子类必须实现reset方法")

    def end(self):
        """结束任务"""
        raise NotImplementedError("子类必须实现end方法")