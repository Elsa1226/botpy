# handle_commands.py
import random

from botpy import logging
from base.session_manager import global_session_manager, SessionManagerError
from constants.command_constants import CommandType, COMMAND_DESCRIPTIONS, RANDOM_REPLY_SUFFIX, \
    MULTI_ROUND_COMMANDS, SINGLE_ROUND_COMMANDS, MULTI_ROUND_VALID_CMDS, MULTI_ROUND_DEFAULT_TEMPLATES
from constants.multi_task_constants import SessionStatus
from function.multiTask.rock_paper_scissors import RockPaperScissorsTask
from function.random.lottery import handle_lottery_command

_log = logging.get_logger()


async def process_user_command(user_openid: str, msg_content: str) -> str:
    """
    统一处理用户指令，返回对应的回复内容
    :param user_openid: 用户openid
    :param msg_content: 用户发送的消息内容（已去除首尾空格）
    :return: 要回复用户的文本内容
    """

    # 会话预检
    session = global_session_manager.get_session(user_openid)
    has_active_session = False
    if session:
        has_active_session = (
                session.session_status == SessionStatus.ACTIVE
                and not session.is_timeout()
        )

    if has_active_session:
        # 2.1 先校验会话超时（兜底）
        timeout_msg = session.handle_timeout()
        if timeout_msg:
            return timeout_msg

        # 2.2 获取当前任务实例和类型
        active_task = session.active_task
        task_type = active_task.task_type.value

        if msg_content == "状态":
            user_openid = session.user_openid
            staus = session.session_status
            active_task = session.active_task
            last_active_time = session.last_active_time
            timeout = session.timeout

            return f"当前任务：{active_task.task_name}\n" \
                   f"状态：{staus}\n" \
                   f"用户：{user_openid}\n" \
                   f"最后活跃时间：{last_active_time}\n" \
                   f"超时时间：{timeout}\n" \
                   f"任务类型：{task_type}\n" \
                   f"任务实例：{active_task}"

        if msg_content == "记录":
            return active_task.get_summary()

        # 2.3 通用退出指令：结束任务
        if msg_content == "结束任务":
            end_prompt = active_task.get_prompt("end") if hasattr(active_task, "get_prompt") else \
                MULTI_ROUND_DEFAULT_TEMPLATES["end"].format(task_name=active_task.task_name)
            session.end_task()  # 结束任务+重置会话状态
            global_session_manager.end_and_archive_session(user_openid, end_type="active_end")
            return end_prompt

        # 2.4 判断是否为当前任务的合法指令
        valid_cmds = active_task.get_valid_cmds() if hasattr(active_task,
                                                             "get_valid_cmds") else MULTI_ROUND_VALID_CMDS.get(
            task_type, [])
        if msg_content in valid_cmds:
            # 2.4.1 处理猜拳任务交互（示例）
            if task_type == "rock_paper_scissors":
                round_result = active_task.play_round(msg_content)
                session.update_active_time()  # 更新活跃时间
                return round_result["msg"]
            # 2.4.2 拓展：其他多轮任务（如猜谜语）
            # elif task_type == "riddle":
            #     return active_task.handle_riddle(msg_content)
            else:
                return f"当前{active_task.task_name}暂未实现该指令处理逻辑"

        # 2.5 非法指令 → 返回阻断提示
        else:
            invalid_prompt = active_task.get_prompt("invalid_cmd") if hasattr(active_task, "get_prompt") else \
                MULTI_ROUND_DEFAULT_TEMPLATES["invalid_cmd"].format(
                    task_name=active_task.task_name,
                    valid_cmds="、".join(valid_cmds)
                )
            return invalid_prompt

    # 彩票
    if msg_content.startswith((CommandType.LOTTERY_SUPER_LOTTO.value,
                               CommandType.LOTTERY_DOUBLE_COLOR.value)):
        return handle_lottery_command(msg_content)

    if msg_content in SINGLE_ROUND_COMMANDS:
        # 帮助
        if msg_content == CommandType.BASE_HELP.value:
            # 拼接帮助信息（从常量字典中自动读取）
            help_text = "📖 支持的指令列表：\n"
            for cmd, desc in COMMAND_DESCRIPTIONS.items():
                help_text += f"• {cmd}：{desc}\n"
            return help_text

        # 我是谁
        elif msg_content == CommandType.BASE_WHOAMI.value:
            return f"【你的user_id】\n{user_openid}"

        # 其他所有消息返回默认内容
        else:
            random_suffix = random.choice(RANDOM_REPLY_SUFFIX)
            return f"我收到了你的消息：{msg_content}{random_suffix}"

    elif msg_content in MULTI_ROUND_COMMANDS:
        try:
            # 创建多轮任务会话
            session = global_session_manager.create_session(user_openid)
        except SessionManagerError as e:
            # 仅捕获「会话已存在」的异常，兜底提示
            return f"⚠️ 操作失败：{str(e)}\n你当前已有未结束的任务，请先发送「结束任务」退出后再尝试～"

        # 2. 具体业务逻辑（无需捕获异常，移出try块）
        if msg_content == CommandType.GAME_ROCK_PAPER_SCISSORS.value:
            guess_task = RockPaperScissorsTask()
            session.activate_task(guess_task)
            start_prompt = guess_task.get_prompt("start")
            return start_prompt

        # 其他所有消息返回默认内容
        else:
            random_suffix = random.choice(RANDOM_REPLY_SUFFIX)
            return f"我收到了你的消息：{msg_content}{random_suffix}"


    # 其他所有消息返回默认内容
    else:
        random_suffix = random.choice(RANDOM_REPLY_SUFFIX)
        return f"我收到了你的消息：{msg_content}{random_suffix}"
