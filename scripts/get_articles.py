import os
import argparse
import requests
from datetime import datetime, date, timedelta, timezone
from dotenv import load_dotenv

load_dotenv()

PAGE_LIMIT = 20

def get_articles(target_date: str = None, mp_id: str = None):
    """
    获取文章列表（自动分页，筛选指定日期的文章）

    参数:
        target_date (str): 目标日期，格式 YYYY-MM-DD，默认为当天
        mp_id (str): 所属公众号 ID，可选

    返回:
        list: 符合条件的文章列表，每篇文章包含 id, created_at, description, title, mp_name, publish_time 字段
    """
    access_key = os.getenv("ACCESS_KEY")
    secret_key = os.getenv("SECRET_KEY")
    base_url = os.getenv("BASE_URL")

    if not access_key or not secret_key or not base_url:
        raise ValueError("请确保在 .env 文件中配置了 ACCESS_KEY, SECRET_KEY 和 BASE_URL")

    if target_date is None:
        target_date = datetime.now(timezone(timedelta(hours=8))).strftime("%Y-%m-%d")

    try:
        target_date_obj = datetime.strptime(target_date, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError("target_date 格式必须为 YYYY-MM-DD")

    beijing_tz = timezone(timedelta(hours=8))
    start_ts = datetime(target_date_obj.year, target_date_obj.month, target_date_obj.day, 0, 0, 0, tzinfo=beijing_tz).timestamp()
    end_ts = datetime(target_date_obj.year, target_date_obj.month, target_date_obj.day, 23, 59, 59, tzinfo=beijing_tz).timestamp()

    headers = {
        "Authorization": f"AK-SK {access_key}:{secret_key}"
    }

    url = f"{base_url}/api/v1/wx/articles"

    matched_articles = []
    offset = 0

    while True:
        params = {
            "offset": offset,
            "limit": PAGE_LIMIT,
        }

        if mp_id is not None:
            params["mp_id"] = mp_id

        response = requests.get(url, headers=headers, params=params, timeout=10)

        if response.status_code == 422:
            print("参数错误:", response.json())
            response.raise_for_status()

        response.raise_for_status()
        data = response.json().get("data")

        articles = []
        if isinstance(data, list):
            articles = data
        elif isinstance(data, dict) and "list" in data:
            articles = data["list"]

        if not articles:
            break

        has_match_in_page = False
        for article in articles:
            publish_time = article.get("publish_time")
            if not publish_time:
                continue

            try:
                pt = int(publish_time)
                if start_ts <= pt <= end_ts:
                    has_match_in_page = True
                    matched_articles.append({
                        "id": article.get("id"),
                        "created_at": article.get("created_at"),
                        "description": article.get("description"),
                        "title": article.get("title"),
                        "mp_name": article.get("mp_name"),
                        "publish_time": article.get("publish_time")
                    })
            except (ValueError, TypeError):
                continue

        if not has_match_in_page:
            break

        offset += PAGE_LIMIT

    return matched_articles

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="获取微信公众号文章列表")
    parser.add_argument("--date", type=str, default=None, help="目标日期，格式 YYYY-MM-DD，默认为当天")
    parser.add_argument("--mp_id", type=str, default=None, help="公众号 ID，可选")
    parser.add_argument("--show-id", action="store_true", help="显示文章 ID")
    args = parser.parse_args()
    
    try:
        print("正在获取文章列表...")
        result = get_articles(target_date=args.date, mp_id=args.mp_id)
        print(f"获取到 {len(result)} 篇文章:")
        for article in result:
            if args.show_id:
                print(f"  - [{article['id']}] {article['title']} ({article['created_at']})")
            else:
                print(f"  - {article['title']} ({article['created_at']})")
    except Exception as e:
        print(f"请求失败：{e}")
