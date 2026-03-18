# lottery.py
import random


def generate_lottery_super_lotto():
    """生成一注超级大乐透号码"""
    # 前区35选5，排序并格式化为两位数
    front_numbers = random.sample(range(1, 36), 5)
    front_numbers.sort()
    front_formatted = [f"{num:02d}" for num in front_numbers]

    # 后区12选2，排序并格式化为两位数
    back_numbers = random.sample(range(1, 13), 2)
    back_numbers.sort()
    back_formatted = [f"{num:02d}" for num in back_numbers]

    return {
        "前区": " ".join(front_formatted),
        "后区": " ".join(back_formatted),
        "注数": 1,
        "单注金额": "2元（追加+1元）"
    }


def generate_lottery_double_color():
    """生成一注双色球号码"""
    # 红球33选6，排序并格式化为两位数
    red_numbers = random.sample(range(1, 34), 6)
    red_numbers.sort()
    red_formatted = [f"{num:02d}" for num in red_numbers]

    # 蓝球16选1，格式化为两位数
    blue_number = random.randint(1, 16)
    blue_formatted = f"{blue_number:02d}"

    return {
        "红球": " ".join(red_formatted),
        "蓝球": blue_formatted,
        "注数": 1,
        "单注金额": "2元"
    }


def handle_lottery_command(msg_content):
    """
    统一处理彩票指令，返回格式化的回复内容
    :param msg_content: 用户发送的消息内容
    :return: 回复字符串
    """
    # 去除首尾空格
    msg = msg_content.strip()

    # 处理超级大乐透指令
    if msg.startswith("超级大乐透"):
        try:
            # 解析注数
            parts = msg.split()
            n = int(parts[1]) if (len(parts) >= 2 and parts[1].isdigit()) else 1
            # 限制注数范围：1-10
            n = max(1, min(n, 10))

            # 生成n注号码并格式化
            reply = f"🎟️ 超级大乐透（共{n}注）：\n"
            for i in range(n):
                lottery = generate_lottery_super_lotto()
                reply += f"第{i + 1}注：前区 {lottery['前区']} | 后区 {lottery['后区']}\n"
            return reply
        except Exception as e:
            return f"❌ 超级大乐透指令错误：请发送「超级大乐透 n」（n为1-10的数字），例如「超级大乐透 5」\n错误详情：{str(e)}"

    # 处理双色球指令
    elif msg.startswith("双色球"):
        try:
            # 解析注数
            parts = msg.split()
            n = int(parts[1]) if (len(parts) >= 2 and parts[1].isdigit()) else 1
            # 限制注数范围：1-10
            n = max(1, min(n, 10))

            # 生成n注号码并格式化
            reply = f"🎟️ 双色球（共{n}注）：\n"
            for i in range(n):
                lottery = generate_lottery_double_color()
                reply += f"第{i + 1}注：红球 {lottery['红球']} | 蓝球 {lottery['蓝球']}\n"
            return reply
        except Exception as e:
            return f"❌ 双色球指令错误：请发送「双色球 n」（n为1-10的数字），例如「双色球 5」\n错误详情：{str(e)}"

    # 非彩票指令返回空，交给主函数处理
    else:
        return None