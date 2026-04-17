import os
import argparse
import requests
from dotenv import load_dotenv

load_dotenv()

def get_article_details(article_id: str):
    """
    获取文章详情

    参数:
        article_id (str): 文章 ID

    返回:
        dict: 文章详情数据
    """
    access_key = os.getenv("ACCESS_KEY")
    secret_key = os.getenv("SECRET_KEY")
    base_url = os.getenv("BASE_URL")

    if not access_key or not secret_key or not base_url:
        raise ValueError("请确保在 .env 文件中配置了 ACCESS_KEY, SECRET_KEY 和 BASE_URL")

    headers = {
        "Authorization": f"AK-SK {access_key}:{secret_key}"
    }

    url = f"{base_url}/api/v1/wx/articles/{article_id}"

    response = requests.get(url, headers=headers, timeout=10)

    if response.status_code == 422:
        response.raise_for_status()

    response.raise_for_status()
    return response.json().get("data")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="获取微信公众号文章详情")
    parser.add_argument("article_id", type=str, help="文章 ID")
    args = parser.parse_args()
    
    try:
        print("正在获取文章详情...")
        result = get_article_details(args.article_id)
        print("获取结果:")
        print(result)
    except Exception as e:
        print(f"请求失败：{e}")
