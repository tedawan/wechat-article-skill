#!/usr/bin/env python3
"""
微信公众号订阅和文章管理工具 - 主入口

支持命令：
- subscribe: 订阅公众号
- list_subs: 获取已订阅公众号列表
- unsubscribe: 删除订阅公众号
- articles: 获取特定日期的文章
- article_detail: 获取文章详情
"""

import sys
import os
import json
from datetime import datetime, timezone, timedelta

# 添加 scripts 目录到路径
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)


def print_usage():
    """打印使用说明"""
    print("""
微信公众号订阅和文章管理工具

用法:
    python main.py <command> [options]

命令:
    subscribe <公众号名称>     订阅公众号
    list_subs [关键词]        获取已订阅公众号列表
    unsubscribe <公众号名称>   删除订阅公众号
    articles [日期]           获取特定日期的文章 (YYYY-MM-DD)
    article_detail <id>       获取文章详情

选项:
    --help, -h               显示帮助

示例:
    python main.py subscribe 虎嗅 APP
    python main.py list_subs
    python main.py list_subs 虎嗅
    python main.py unsubscribe 虎嗅 APP
    python main.py articles 2026-04-16
    python main.py article_detail article_id_123
""")


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ["-h", "--help"]:
        print_usage()
        return

    command = sys.argv[1]

    try:
        if command == "subscribe":
            if len(sys.argv) < 3:
                print(json.dumps({"success": False, "error": "请提供公众号名称"}, ensure_ascii=False))
                return
            from add_mp import add_mp
            mp_name = sys.argv[2]
            result = add_mp(mp_name)
            print(json.dumps({"success": True, "data": result}, ensure_ascii=False))

        elif command == "list_subs":
            from list_mps import list_mps
            kw = sys.argv[2] if len(sys.argv) > 2 else ""
            result = list_mps(kw=kw)
            print(json.dumps({"success": True, "data": result}, ensure_ascii=False, indent=2))

        elif command == "unsubscribe":
            if len(sys.argv) < 3:
                print(json.dumps({"success": False, "error": "请提供公众号名称"}, ensure_ascii=False))
                return
            from delete_mp import delete_mp
            mp_name = sys.argv[2]
            result = delete_mp(mp_name)
            print(json.dumps({"success": True, "data": result}, ensure_ascii=False))

        elif command == "articles":
            date = sys.argv[2] if len(sys.argv) > 2 else None
            from get_articles import get_articles
            result = get_articles(target_date=date)

            for article in result:
                if article.get('publish_time'):
                    try:
                        pt = int(article['publish_time'])
                        article['publish_time'] = datetime.fromtimestamp(pt, tz=timezone(timedelta(hours=8))).strftime('%Y-%m-%d %H:%M:%S')
                    except (ValueError, TypeError):
                        pass

            print(json.dumps(result, ensure_ascii=False, indent=2))

        elif command == "article_detail":
            if len(sys.argv) < 3:
                print(json.dumps({"success": False, "error": "请提供文章 ID"}, ensure_ascii=False))
                return
            from get_article_details import get_article_details
            article_id = sys.argv[2]
            result = get_article_details(article_id)
            print(json.dumps(result, ensure_ascii=False, indent=2))

        else:
            print(json.dumps({"success": False, "error": f"未知命令：{command}"}, ensure_ascii=False))

    except Exception as e:
        print(json.dumps({"success": False, "error": str(e)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
