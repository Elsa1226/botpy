# command_constants.py
from enum import Enum, unique

# 指令类型枚举（按功能分类）
@unique
class CommandType(Enum):
    """指令类型枚举"""
    # ========== 单次对话指令 ==========
    # 彩票相关
    LOTTERY_SUPER_LOTTO = "超级大乐透"
    LOTTERY_DOUBLE_COLOR = "双色球"
    # 工具
    TOOL_BASE64 = "BASE64编解码"
    # 基础功能
    BASE_WHOAMI = "我是谁"
    BASE_HELP = "帮助"
    BASE_ABOUT = "关于"

    # ========== 多轮对话基础指令 ==========
    MULT_BASE_STATUS = "状态"
    MULT_BASE_RECORD = "记录"
    MULT_BASE_END_MISSION = "结束任务"

    # ========== 多轮对话后端指令 ==========
    MULT_BASE_START = "mult_base_start"
    MULT_BASE_END = "mult_base_end"
    MULT_BASE_TIMEOUT = "mult_base_timeout"
    MULT_BASE_SUMMARY = "mult_base_summary"
    MULT_BASE_INVALID_CMD = "mult_base_invalid_cmd"

    # ========== 多轮对话指令 ==========
    GAME_ROCK_PAPER_SCISSORS = "猜拳"  # 猜拳游戏

# ========== 指令分类集合 ==========
# 单次对话指令集合
SINGLE_ROUND_COMMANDS = {
    CommandType.LOTTERY_SUPER_LOTTO.value,
    CommandType.LOTTERY_DOUBLE_COLOR.value,
    CommandType.TOOL_BASE64.value,
    CommandType.BASE_WHOAMI.value,
    CommandType.BASE_HELP.value,
    CommandType.BASE_ABOUT.value
}

# 多轮对话指令集合
MULTI_BASE_COMMANDS = {
    CommandType.MULT_BASE_STATUS.value,
    CommandType.MULT_BASE_RECORD.value,
    CommandType.MULT_BASE_END_MISSION.value
}

# 多轮对话后端指令
MULTI_BASE_BACKEND_COMMANDS = {
    CommandType.MULT_BASE_START.value,
    CommandType.MULT_BASE_END.value,
    CommandType.MULT_BASE_TIMEOUT.value,
    CommandType.MULT_BASE_SUMMARY.value,
    CommandType.MULT_BASE_INVALID_CMD.value
}

# 多轮对话指令集合
MULTI_ROUND_COMMANDS = {
    CommandType.GAME_ROCK_PAPER_SCISSORS.value
}

# 所有指令前缀（合并两类，用于快速判断）
COMMAND_PREFIXES = SINGLE_ROUND_COMMANDS | MULTI_ROUND_COMMANDS

# ========== 指令描述（补充多轮指令说明） ==========
COMMAND_DESCRIPTIONS = {
    # 单次指令
    CommandType.LOTTERY_SUPER_LOTTO.value: "生成超级大乐透号码，格式：超级大乐透 [1-10]（默认1注）",
    CommandType.LOTTERY_DOUBLE_COLOR.value: "生成双色球号码，格式：双色球 [1-10]（默认1注）",
    CommandType.TOOL_BASE64.value: "BASE64编解码（多轮），格式：BASE64编解码 编码/解码 内容",
    CommandType.BASE_WHOAMI.value: "查看当前用户信息",
    CommandType.BASE_HELP.value: "查看所有支持的指令",
    CommandType.BASE_ABOUT.value: "查看机器人介绍",
    # 多轮指令
    CommandType.GAME_ROCK_PAPER_SCISSORS.value: "猜拳游戏（多轮），发送「猜拳」开始游戏，支持：石头/剪刀/布"
}

MULT_BASE_START = "mult_base_start"
MULT_BASE_END = "mult_base_end"
MULT_BASE_TIMEOUT = "mult_base_timeout"
MULT_BASE_SUMMARY = "mult_base_summary"
MULT_BASE_INVALID_CMD = "mult_base_invalid_cmd"

# ========== 新增：多轮任务文本模板 ==========
# 通用模板（所有多轮任务默认使用）
MULTI_ROUND_DEFAULT_TEMPLATES = {
    "mult_base_start": "【{task_name}】已启动！请发送任务内指令，或发送「结束任务」退出～",
    "mult_base_end": "【{task_name}】已结束！",
    "mult_base_timeout": "⚠️ 【{task_name}】会话超时，已自动结束～",
    "mult_base_invalid_cmd": "❌ 当前仅支持【{task_name}】的指令：{valid_cmds}，或发送「结束任务」退出～"
}

# 任务专属模板（按需覆盖通用模板）
MULTI_ROUND_TASK_TEMPLATES = {
    # 猜拳任务
    CommandType.GAME_ROCK_PAPER_SCISSORS.value: {
        "mult_base_start": "✊ 猜拳游戏开始！可发送：石头/剪刀/布，或「结束任务」退出～",
        "mult_base_end": "🎮 猜拳游戏结束！共玩{round_num}轮，你赢{user_win}轮～",  # 支持动态参数
        "mult_base_valid_cmds": "石头、剪刀、布"
    },
    # # 猜谜语任务（未来扩展）
    # CommandType.GAME_RIDDLE.value: {
    #     "start": "🧩 猜谜语游戏开始！请猜谜：{riddle_content}，或发送「结束任务」退出～",
    #     "valid_cmds": "谜底答案"
    # }
}

# 任务合法指令映射
MULTI_ROUND_VALID_CMDS = {
    CommandType.GAME_ROCK_PAPER_SCISSORS.value: ["石头", "剪刀", "布", "结束任务"],
}

# 随机回复后缀列表
RANDOM_REPLY_SUFFIX = [
    "，但是不想理你😜",
    "，但是不明白你在说什么🤔",
    "，要不换个指令试试？👉 发送「帮助」查看支持的指令",
    "，我有点懵懵的～😵",
    "，虽然收到了，但我选择装没看见😝",
    "，你说的这个我还不会呢😭",
    "，其实我不是人工智能哦😁",
]