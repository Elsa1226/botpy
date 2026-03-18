# -*- coding: utf-8 -*-
import asyncio
import os

import botpy
from botpy import logging
from botpy.ext.cog_yaml import read
from botpy.message import C2CMessage
from command_constants import CommandType, COMMAND_DESCRIPTIONS

# 导入彩票模块的统一处理函数
from funtion.random.lottery import handle_lottery_command

test_config = read(os.path.join(os.path.dirname(__file__), "config.yaml"))

_log = logging.get_logger()


class MyClient(botpy.Client):
    async def on_ready(self):
        _log.info(f"robot 「{self.robot.name}」 on_ready!")

    async def on_c2c_message_create(self, message: C2CMessage):
        # 获取用户消息内容并去除首尾空格
        msg_content = message.content.strip()

        # 处理彩票指令
        if msg_content.startswith((CommandType.LOTTERY_SUPER_LOTTO.value,
                                   CommandType.LOTTERY_DOUBLE_COLOR.value)):
            reply_content = handle_lottery_command(msg_content)
        # 处理帮助指令
        elif msg_content == CommandType.BASE_HELP.value:
            # 拼接帮助信息（从常量字典中自动读取）
            help_text = "📖 支持的指令列表：\n"
            for cmd, desc in COMMAND_DESCRIPTIONS.items():
                help_text += f"• {cmd}：{desc}\n"
            reply_content = help_text
        # 其他所有消息返回默认内容
        else:
            reply_content = f"我收到了你的消息：{msg_content}"

        # 统一发送回复
        await message._api.post_c2c_message(
            openid=message.author.user_openid,
            msg_type=0,
            msg_id=message.id,
            content=reply_content
        )


if __name__ == "__main__":
    intents = botpy.Intents(public_messages=True)
    client = MyClient(intents=intents)
    client.run(appid=test_config["appid"], secret=test_config["secret"])
