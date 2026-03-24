from datetime import datetime
from typing import Optional
from constants.multi_task_constants import SessionStatus
from base.base_task import BaseTask


class UserSession:
    """用户会话类（通用）"""

    def __init__(self, user_openid: str, timeout: int = 300):
        self.user_openid = user_openid  # 用户唯一ID
        self.session_status = SessionStatus.IDLE  # 初始状态
        self.active_task: Optional[BaseTask] = None  # 当前激活的任务（可选类型）
        self.last_active_time = datetime.now()  # 最后活跃时间
        self.timeout = timeout  # 超时阈值（秒）

    def update_active_time(self):
        """更新最后活跃时间"""
        self.last_active_time = datetime.now()

    def is_timeout(self) -> bool:
        """判断是否超时"""
        time_diff = datetime.now() - self.last_active_time
        return time_diff.total_seconds() > self.timeout

    def activate_task(self, task: BaseTask):
        """激活新任务"""
        self.active_task = task
        self.session_status = SessionStatus.ACTIVE
        self.update_active_time()

    def end_task(self) -> str:
        """结束当前任务"""
        if not self.active_task:
            return "当前无正在进行的任务！"

        self.active_task.end()
        # 增加类型检查，避免调用不存在的方法时出错
        summary = self.active_task.get_summary() if hasattr(self.active_task, "get_summary") else "任务已结束！"

        self.active_task = None
        self.session_status = SessionStatus.FINISHED
        self.update_active_time()
        return summary

    def reset(self):
        """重置会话"""
        self.session_status = SessionStatus.IDLE
        self.active_task = None
        self.last_active_time = datetime.now()

    def handle_timeout(self) -> str:
        """处理超时"""
        if self.is_timeout() and self.session_status == SessionStatus.ACTIVE:
            self.session_status = SessionStatus.TIMEOUT
            if self.active_task:
                self.active_task.end()
                self.active_task = None
            return "⚠️ 会话超时！已自动结束当前任务～"
        return ""
