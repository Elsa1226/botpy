import json
import os
from datetime import datetime
from base.user_session import UserSession
from constants.multi_task_constants import TaskType


class SessionArchive:
    """会话归档工具：将结束/超时的会话保存到文件，支持按日期/用户归档"""

    def __init__(self, archive_dir: str = "session_archives"):
        # 归档目录（自动创建）
        self.archive_dir = archive_dir
        if not os.path.exists(self.archive_dir):
            os.makedirs(self.archive_dir)

    def _generate_session_id(self, user_openid: str) -> str:
        """生成唯一会话ID（用户ID+时间戳）"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        return f"{user_openid}_{timestamp}"

    def _serialize_session(self, session: UserSession, end_type: str) -> dict:
        """序列化会话数据（提取核心字段）"""
        # 基础信息
        serialized = {
            "session_id": self._generate_session_id(session.user_openid),
            "user_openid": session.user_openid,
            "start_time": session.last_active_time.strftime("%Y-%m-%d %H:%M:%S"),  # 启动时间=首次活跃时间
            "end_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "end_type": end_type,  # "active_end"（主动结束）/ "timeout"（超时）
            "task_type": None,
            "task_data": {},
            "message_history": []
        }

        # 提取任务相关数据（按需扩展）
        if session.active_task:
            serialized["task_type"] = session.active_task.task_type.value
            # 猜拳任务数据
            if serialized["task_type"] == TaskType.RockPaperScissors.value:
                serialized["task_data"] = {
                    "round_num": session.active_task.round_num,
                    "user_win": session.active_task.user_win,
                    "bot_win": session.active_task.bot_win,
                    "draw_num": session.active_task.draw_num
                }
            # 拓展：其他任务（如猜谜语）
            # elif serialized["task_type"] == "riddle":
            #     serialized["task_data"] = {...}

        return serialized

    def archive_session(self, session: UserSession, end_type: str):
        """
        归档会话：序列化后写入文件
        :param session: 要归档的UserSession实例
        :param end_type: 结束类型（active_end/timeout）
        """
        # 1. 序列化
        session_data = self._serialize_session(session, end_type)
        # 2. 按日期分文件（避免单文件过大）
        date_str = datetime.now().strftime("%Y%m%d")
        file_path = os.path.join(self.archive_dir, f"session_archive_{date_str}.json")
        # 3. 写入文件（追加模式，每行一个JSON）
        with open(file_path, "a", encoding="utf-8") as f:
            json.dump(session_data, f, ensure_ascii=False)
            f.write("\n")  # 换行分隔，便于后续读取

    def read_archive(self, date_str: str = None) -> list:
        """读取归档数据（按日期，默认读取今日）"""
        if not date_str:
            date_str = datetime.now().strftime("%Y%m%d")
        file_path = os.path.join(self.archive_dir, f"session_archive_{date_str}.json")
        if not os.path.exists(file_path):
            return []
        # 读取所有行（每行一个会话）
        with open(file_path, "r", encoding="utf-8") as f:
            return [json.loads(line) for line in f.readlines()]


# 全局归档实例
global_session_archive = SessionArchive()