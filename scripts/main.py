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

# 添加 scripts 目录到路径
SCRIPT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scripts')
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

    if command == "subscribe":
        if len(sys.argv) < 3:
            print("请提供公众号名称")
            return
        from add_mp import add_mp
        mp_name = sys.argv[2]
        result = add_mp(mp_name)
        print(f"订阅结果：{result}")

    elif command == "list_subs":
        from list_mps import list_mps
        kw = sys.argv[2] if len(sys.argv) > 2 else ""
        result = list_mps(kw=kw)
        print("已订阅公众号列表:")
        print(result)

    elif command == "unsubscribe":
        if len(sys.argv) < 3:
            print("请提供公众号名称")
            return
        from delete_mp import delete_mp
        mp_name = sys.argv[2]
        result = delete_mp(mp_name)
        print(f"删除结果：{result}")

    elif command == "articles":
        date = sys.argv[2] if len(sys.argv) > 2 else None
        from get_articles import get_articles
        result = get_articles(target_date=date)
        print(f"获取到 {len(result)} 篇文章:")
        for i, article in enumerate(result, 1):
            print(f"{i}. {article['title']} - {article['mp_name']}")

    elif command == "article_detail":
        if len(sys.argv) < 3:
            print("请提供文章 ID")
            return
        from get_article_details import get_article_details
        article_id = sys.argv[2]
        result = get_article_details(article_id)
        print("文章详情:")
        print(result)

    else:
        print(f"未知命令：{command}")
        print_usage()


if __name__ == "__main__":
    main()
