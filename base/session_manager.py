from base.session_archive import global_session_archive
from base.user_session import UserSession
from constants.multi_task_constants import SessionStatus


class SessionManagerError(Exception):
    """会话管理器专属异常（自定义，便于定位问题）"""
    pass


class SessionManager:
    """会话管理器（全局管控用户会话）- 严格拆分查询/创建，创建重复抛异常"""

    def __init__(self):
        self.session_map = {}  # {user_openid: UserSession}

    def get_session(self, user_openid: str) -> UserSession | None:
        """纯查询：获取用户会话（不存在则返回None，不创建）"""
        return self.session_map.get(user_openid)

    def create_session(self, user_openid: str) -> UserSession:
        """
        纯创建：创建用户会话
        严格保证：仅当会话不存在时创建，已存在则抛异常（符合业务逻辑）
        """
        if user_openid in self.session_map:
            raise SessionManagerError(f"用户[{user_openid}]的会话已存在，禁止重复创建！")

        new_session = UserSession(user_openid)
        self.session_map[user_openid] = new_session
        return new_session

    def get_or_create_session(self, user_openid: str) -> UserSession:
        """兼容方法：查询+创建（保留，供特殊场景使用）"""
        session = self.get_session(user_openid)
        if not session:
            session = self.create_session(user_openid)
        return session

    def end_and_archive_session(self, user_openid: str, end_type: str = "active_end"):
        """
        结束并归档会话（核心方法）
        :param user_openid: 用户ID
        :param end_type: 结束类型（active_end/timeout）
        """
        session = self.get_session(user_openid)
        if not session:
            return

        # 1. 归档会话（保存到文件）
        global_session_archive.archive_session(session, end_type)
        # 2. 从内存移除会话（删除实例）
        self.remove_session(user_openid)

    def clean_timeout_sessions(self):
        """清理超时会话（归档+移除）"""
        timeout_users = []
        for openid, session in self.session_map.items():
            if session.is_timeout() and session.session_status == SessionStatus.ACTIVE:
                timeout_users.append(openid)
                # 归档超时会话
                self.end_and_archive_session(openid, end_type="timeout")
        return f"清理并归档了{len(timeout_users)}个超时会话"

    def remove_session(self, user_openid: str):
        """纯移除：从内存删除会话实例"""
        if user_openid in self.session_map:
            del self.session_map[user_openid]


# 全局会话管理器实例（单例）
global_session_manager = SessionManager()
