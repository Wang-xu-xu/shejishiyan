"""联网搜索模块 — 搜索设计素材"""

import urllib.request
import urllib.parse
import json
import re


def search_unsplash(query: str, count: int = 6) -> list[dict]:
    """搜索 Unsplash 免费图片素材"""
    results = []
    try:
        url = f"https://unsplash.com/napi/search/photos?query={urllib.parse.quote(query)}&per_page={count}"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0", "Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
        for item in data.get("results", []):
            results.append({
                "title": item.get("alt_description", "无标题"),
                "thumb": item["urls"]["thumb"],
                "full":  item["urls"]["regular"],
                "author": item["user"]["name"],
                "source": "Unsplash",
            })
    except Exception as e:
        print(f"[搜索提示] Unsplash 请求失败: {e}")
    return results


def search_pexels(query: str, count: int = 6) -> list[dict]:
    """搜索 Pexels 免费素材"""
    results = []
    try:
        url = f"https://www.pexels.com/zh-cn/search/{urllib.parse.quote(query)}/"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode("utf-8")
        # 从页面提取图片 URL
        imgs = re.findall(r'data-src="(https://images\.pexels\.com/photos/\d+/[^"]+)"', html)
        seen = set()
        for img in imgs:
            photo_id = img.split("/")[4]
            if photo_id not in seen:
                seen.add(photo_id)
                results.append({
                    "title": f"Pexels-{photo_id}",
                    "thumb": img + "?auto=compress&w=400",
                    "full":  img,
                    "author": "Pexels",
                    "source": "Pexels",
                })
            if len(results) >= count:
                break
    except Exception as e:
        print(f"[搜索提示] Pexels 请求失败: {e}")
    return results


def search_icons(query: str, count: int = 6) -> list[dict]:
    """搜索 SVG 图标 (Iconify)"""
    results = []
    try:
        url = f"https://api.iconify.design/search?query={urllib.parse.quote(query)}&limit={count}"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
        for icon_set in data.get("icons", []):
            prefix, name = icon_set.split(":", 1)
            results.append({
                "title": name,
                "thumb": f"https://api.iconify.design/{prefix}/{name}.svg",
                "full":  f"https://api.iconify.design/{prefix}/{name}.svg",
                "author": prefix,
                "source": "Iconify (SVG)",
            })
    except Exception as e:
        print(f"[搜索提示] Iconify 请求失败: {e}")
    return results


def search_material(query: str, material_type: str = "all") -> dict:
    """统一搜索入口，按素材类型分发"""
    results = {
        "query": query,
        "type": material_type,
        "images": [],
        "icons": [],
    }
    if material_type in ("all", "image"):
        results["images"] = search_unsplash(query) or search_pexels(query)
    if material_type in ("all", "icon"):
        results["icons"] = search_icons(query)
    return results


def format_results(results: dict) -> str:
    """格式化搜索结果输出"""
    lines = [f"\n搜索结果: {results['query']} (类型: {results['type']})", "=" * 50]
    if results["images"]:
        lines.append(f"\n📷 图片素材 ({len(results['images'])} 个):")
        for i, img in enumerate(results["images"], 1):
            lines.append(f"  {i}. {img['title']}")
            lines.append(f"     来源: {img['source']} | {img['author']}")
            lines.append(f"     预览: {img['thumb']}")
    if results["icons"]:
        lines.append(f"\n🎯 SVG 图标 ({len(results['icons'])} 个):")
        for i, icon in enumerate(results["icons"], 1):
            lines.append(f"  {i}. {icon['title']} ({icon['author']})")
            lines.append(f"     SVG: {icon['full']}")
    if not results["images"] and not results["icons"]:
        lines.append("\n未找到相关素材，请尝试其他关键词。")
    return "\n".join(lines)
