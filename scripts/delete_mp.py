import os
import requests
from dotenv import load_dotenv

load_dotenv()

def delete_mp(mp_name: str):
    """
    删除公众号

    参数:
        mp_name (str): 公众号名称

    返回:
        str: API 响应结果
    """
    from list_mps import list_mps

    access_key = os.getenv("ACCESS_KEY")
    secret_key = os.getenv("SECRET_KEY")
    base_url = os.getenv("BASE_URL")

    if not access_key or not secret_key or not base_url:
        raise ValueError("请确保在 .env 文件中配置了 ACCESS_KEY, SECRET_KEY 和 BASE_URL")

    # 先从已订阅列表中查找该公众号
    print(f"正在查找公众号：{mp_name}...")
    list_result = list_mps(kw=mp_name, limit=100)

    if not list_result:
        print(f"未找到公众号：{mp_name}")
        return None

    # 从已订阅列表中提取 mp_id
    mp_id = None
    mp_list = []
    if isinstance(list_result, list):
        mp_list = list_result
    elif isinstance(list_result, dict) and "list" in list_result:
        mp_list = list_result["list"]
    
    for mp in mp_list:
        if mp.get("mp_name") == mp_name:
            mp_id = mp.get("id")  # 使用 "id" 而不是 "mp_id"
            break

    if not mp_id:
        print(f"未找到公众号：{mp_name}")
        return None

    print(f"找到公众号：{mp_name} (mp_id: {mp_id})")
    print(f"正在删除公众号...")

    headers = {
        "Authorization": f"AK-SK {access_key}:{secret_key}"
    }

    url = f"{base_url}/api/v1/wx/mps/{mp_id}"

    response = requests.delete(url, headers=headers, timeout=10)

    if response.status_code == 422:
        print("参数错误:", response.json())
        response.raise_for_status()

    response.raise_for_status()
    result = response.text
    print(f"删除结果：{result}")
    return result

if __name__ == "__main__":
    try:
        print("正在删除公众号...")
        mp_name_test = "虎嗅 APP"
        result = delete_mp(mp_name_test)
        print("删除结果:")
        print(result)
    except Exception as e:
        print(f"请求失败：{e}")
