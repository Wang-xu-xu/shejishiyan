"""设计自动化 — 命令识别与联网搜索系统"""

COMMANDS = {
    "搜索素材": {"keywords": ["搜索", "素材", "找", "图片", "图标", "矢量", "下载"], "desc": "联网搜索设计素材"},
    "格式转换": {"keywords": ["转换", "转", "导出", "格式"], "desc": "文件格式转换"},
    "生成矢量": {"keywords": ["矢量", "SVG", "矢量化", "描摹"], "desc": "位图转矢量"},
    "设计模板": {"keywords": ["模板", "海报", "名片", "banner"], "desc": "获取设计模板"},
    "帮助":    {"keywords": ["帮助", "help", "功能", "能做什么"], "desc": "显示帮助信息"},
}


def parse_command(text: str) -> str | None:
    """识别用户输入的命令"""
    text_lower = text.strip().lower()
    scores = {}
    for name, cmd in COMMANDS.items():
        score = sum(1 for kw in cmd["keywords"] if kw in text_lower)
        if score > 0:
            scores[name] = score
    if not scores:
        return None
    return max(scores, key=scores.get)


def get_help() -> str:
    lines = ["可用命令："]
    for name, cmd in COMMANDS.items():
        lines.append(f"  {name} — {cmd['desc']}")
    return "\n".join(lines)
