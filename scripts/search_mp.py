import os
import requests
from dotenv import load_dotenv

# 加载 .env 配置文件
load_dotenv()

def search_mps(kw: str, limit: int = 10, offset: int = 0):
    """
    搜索微信公众号
    
    参数:
        kw (str): 搜索关键字
        limit (int): 返回结果的最大数量，默认为 10
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
        "offset": offset
    }

    # 根据 OpenAPI 规范构建 URL
    url = f"{base_url}/api/v1/wx/mps/search/{kw}"
    
    response = requests.get(url, headers=headers, params=params, timeout=10)
    
    # 根据 OpenAPI 规范检查返回状态
    if response.status_code == 422:
        print("参数错误:", response.json())
        response.raise_for_status()
        
    response.raise_for_status()
    return response.json().get("data")

if __name__ == "__main__":
    # 简单的测试示例
    try:
        kw = "AI" # 测试关键字
        print(f"正在搜索公众号: {kw}...")
        result = search_mps(kw, limit=5, offset=0)
        print("搜索结果:")
        print(result)
    except Exception as e:
        print(f"请求失败: {e}")
