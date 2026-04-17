import os
import requests
from dotenv import load_dotenv

# 加载 .env 配置文件
load_dotenv()

def list_mps(kw: str = "", limit: int = 10, offset: int = 0):
    """
    列出已关注的公众号列表

    参数:
        kw (str): 搜索关键字，默认为空（获取全部）
        limit (int): 返回结果的最大数量，默认为 10 (1-100)
        offset (int): 偏移量，默认为 0

    返回:
        dict: API 响应中的 data 字段内容
    """
    access_key = os.getenv("ACCESS_KEY")
    secret_key = os.getenv("SECRET_KEY")
    base_url = os.getenv("BASE_URL")

    if not access_key or not secret_key or not base_url:
        raise ValueError("请确保在 .env 文件中配置了 ACCESS_KEY, SECRET_KEY 和 BASE_URL")

    headers = {
        "Authorization": f"AK-SK {access_key}:{secret_key}"
    }

    params = {
        "limit": limit,
        "offset": offset,
    }
    # 仅当 kw 不为空时才加入参数
    if kw:
        params["kw"] = kw

    # 获取已关注的公众号列表 API
    url = f"{base_url}/api/v1/wx/mps"

    response = requests.get(url, headers=headers, params=params, timeout=10)

    # 检查返回状态代码
    if response.status_code == 422:
        response.raise_for_status()

    response.raise_for_status()
    # 返回 data 字段
    return response.json().get("data")

if __name__ == "__main__":
    # 测试示例
    try:
        print("正在获取已关注的公众号列表...")
        result = list_mps(limit=5)
        print("获取结果:")
        print(result)

        print("\n--- 搜索关键字 '虎嗅' ---")
        result = list_mps(kw="虎嗅", limit=5)
        print("搜索结果:")
        print(result)
    except Exception as e:
        print(f"请求失败：{e}")
