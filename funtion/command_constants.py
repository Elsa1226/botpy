# command_constants.py
from enum import Enum, unique

# 指令类型枚举（按功能分类）
@unique
class CommandType(Enum):
    """指令类型枚举（统一管理所有功能分类）"""
    # 彩票相关
    LOTTERY_SUPER_LOTTO = "超级大乐透"  # 超级大乐透
    LOTTERY_DOUBLE_COLOR = "双色球"    # 双色球
    # 工具类（预留扩展）
    TOOL_BASE64 = "BASE64编解码"       # BASE64编解码
    # 基础功能
    BASE_HELP = "帮助"                 # 帮助
    BASE_ABOUT = "关于"                # 关于

# 指令前缀集合（方便快速判断）
COMMAND_PREFIXES = {
    # 彩票指令前缀
    CommandType.LOTTERY_SUPER_LOTTO.value,
    CommandType.LOTTERY_DOUBLE_COLOR.value,
    # 工具指令前缀
    CommandType.TOOL_BASE64.value,
    # 基础指令前缀
    CommandType.BASE_HELP.value,
    CommandType.BASE_ABOUT.value
}

# 扩展：指令描述（用于帮助信息）
COMMAND_DESCRIPTIONS = {
    CommandType.LOTTERY_SUPER_LOTTO.value: "生成超级大乐透号码，格式：超级大乐透 [1-10]（默认1注）",
    CommandType.LOTTERY_DOUBLE_COLOR.value: "生成双色球号码，格式：双色球 [1-10]（默认1注）",
    CommandType.TOOL_BASE64.value: "BASE64编解码，格式：BASE64编解码 编码/解码 内容",
    CommandType.BASE_HELP.value: "查看所有支持的指令",
    CommandType.BASE_ABOUT.value: "查看机器人介绍"
}
