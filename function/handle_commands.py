# handle_commands.py
from botpy import logging
from botpy.message import C2CMessage
from command_constants import CommandType, COMMAND_DESCRIPTIONS
from function.random.lottery import handle_lottery_command

_log = logging.get_logger()


async def process_user_command(user_openid: str, msg_content: str) -> str:
    """
    统一处理用户指令，返回对应的回复内容
    :param msg_content: 用户发送的消息内容（已去除首尾空格）
    :return: 要回复用户的文本内容
    """

    # 处理彩票指令
    if msg_content.startswith((CommandType.LOTTERY_SUPER_LOTTO.value,
                               CommandType.LOTTERY_DOUBLE_COLOR.value)):
        return handle_lottery_command(msg_content)

    # 处理帮助指令
    elif msg_content == CommandType.BASE_HELP.value:
        # 拼接帮助信息（从常量字典中自动读取）
        help_text = "📖 支持的指令列表：\n"
        for cmd, desc in COMMAND_DESCRIPTIONS.items():
            help_text += f"• {cmd}：{desc}\n"
        return help_text

    elif msg_content == CommandType.BASE_WHOAMI.value:
        return f"【你的user_id】\n{user_openid}"


    # 其他所有消息返回默认内容
    else:
        return f"我收到了你的消息：{msg_content}"
