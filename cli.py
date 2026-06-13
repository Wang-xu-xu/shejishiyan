"""设计自动化 CLI — 命令识别 + 联网搜索 + 矢量处理"""

import sys
from commands import parse_command, get_help, COMMANDS
from searcher import search_material, format_results


def handle_search():
    """处理搜索素材命令"""
    query = input("搜索关键词 (如 '蓝色科技'): ").strip()
    if not query:
        print("关键词不能为空")
        return
    print("素材类型: [1] 全部  [2] 图片  [3] SVG图标")
    choice = input("选择 (默认1): ").strip()
    type_map = {"1": "all", "2": "image", "3": "icon"}
    mt = type_map.get(choice, "all")
    print(f"\n正在搜索 {query} ...")
    results = search_material(query, mt)
    print(format_results(results))


def main():
    print("=" * 50)
    print("  设计自动化 v0.1 — 命令识别与素材搜索")
    print("=" * 50)
    print(get_help())
    print("\n输入 'exit' 退出")

    while True:
        try:
            cmd_text = input("\n> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n再见")
            break

        if not cmd_text:
            continue
        if cmd_text.lower() in ("exit", "quit", "q"):
            print("再见")
            break

        cmd = parse_command(cmd_text)
        if cmd is None:
            print("未识别命令，输入 '帮助' 查看可用功能")
            continue

        print(f"[识别] {cmd} — {COMMANDS[cmd]['desc']}")

        if cmd == "搜索素材":
            handle_search()
        elif cmd == "帮助":
            print(get_help())
        elif cmd == "格式转换":
            print("[开发中] 格式转换功能将在后续版本实现")
        elif cmd == "生成矢量":
            print("[开发中] 矢量生成功能将在后续版本实现")
        elif cmd == "设计模板":
            print("[开发中] 设计模板功能将在后续版本实现")
        else:
            print(f"[开发中] {cmd}")


if __name__ == "__main__":
    main()
