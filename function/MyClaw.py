# -*- coding: utf-8 -*-
import asyncio
import os
import time

import botpy
from botpy import logging
from botpy.logging import configure_logging
from logging.handlers import TimedRotatingFileHandler
from botpy.ext.cog_yaml import read
from botpy.message import C2CMessage
from function.handle_commands import process_user_command

test_config = read(os.path.join(os.path.dirname(__file__), "config.yaml"))

current_date = time.strftime("%Y-%m-%d")
log_filename = os.path.join("../logs", f"%(name)s_{current_date}.log")
CUSTOM_FILE_HANDLER = {
    "handler": TimedRotatingFileHandler,
    "backupCount": 0,  # 保留所有日志文件（无上限）
    "filename": log_filename,
    "encoding": "utf-8"
}
configure_logging(ext_handlers=[CUSTOM_FILE_HANDLER])
_log = logging.get_logger()


class MyClient(botpy.Client):
    async def on_ready(self):
        _log.info(f"robot 「{self.robot.name}」 on_ready!")

    async def on_c2c_message_create(self, message: C2CMessage):
        user_openid = message.author.user_openid
        msg_content = message.content.strip()

        _log.info(f"【用户 {user_openid}】发送消息：{msg_content}")

        # 调用独立函数处理指令
        reply_content = await process_user_command(user_openid, msg_content)

        _log.info(f"【机器人 {self.robot.name}】回复用户 {user_openid}：{reply_content}")

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
