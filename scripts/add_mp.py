import os
import requests
from dotenv import load_dotenv

load_dotenv()

def add_mp(mp_name: str, mp_id: str = None, mp_cover: str = None, avatar: str = None, mp_intro: str = None):
    """
    添加公众号

    参数:
        mp_name (str): 公众号名称（必填）
        mp_id (str): 公众号 ID，可选
        mp_cover (str): 公众号封面，可选
        avatar (str): 公众号头像，可选
        mp_intro (str): 公众号介绍，可选

    返回:
        str: API 响应结果
    """
    from search_mp import search_mps

    access_key = os.getenv("ACCESS_KEY")
    secret_key = os.getenv("SECRET_KEY")
    base_url = os.getenv("BASE_URL")

    if not access_key or not secret_key or not base_url:
        raise ValueError("请确保在 .env 文件中配置了 ACCESS_KEY, SECRET_KEY 和 BASE_URL")

    headers = {
        "Authorization": f"AK-SK {access_key}:{secret_key}",
        "Content-Type": "application/json"
    }

    # 如果只传了 mp_name，需要先搜索获取公众号信息
    if mp_id is None and mp_cover is None and avatar is None and mp_intro is None:
        search_result = search_mps(kw=mp_name, limit=1)

        if not search_result:
            return None

        # 获取搜索结果中的第一个公众号信息
        mp_info = None
        if isinstance(search_result, list) and len(search_result) > 0:
            mp_info = search_result[0]
        elif isinstance(search_result, dict) and "list" in search_result:
            mp_list = search_result["list"]
            if mp_list and len(mp_list) > 0:
                mp_info = mp_list[0]

        if not mp_info:
            return None

        mp_id = mp_info.get("fakeid") or mp_info.get("mp_id")
        mp_cover = mp_info.get("round_head_img") or mp_info.get("mp_cover")
        avatar = mp_info.get("round_head_img") or mp_info.get("avatar")
        mp_intro = mp_info.get("signature") or mp_info.get("mp_intro")
        mp_name = mp_info.get("nickname") or mp_name

    # 构建请求体，只包含非空字段
    body = {
        "mp_name": mp_name
    }
    if mp_id is not None:
        body["mp_id"] = mp_id
    if mp_cover is not None:
        body["mp_cover"] = mp_cover
    if avatar is not None:
        body["avatar"] = avatar
    if mp_intro is not None:
        body["mp_intro"] = mp_intro

    url = f"{base_url}/api/v1/wx/mps"

    response = requests.post(url, headers=headers, json=body, timeout=10)

    if response.status_code == 422:
        print("参数错误:", response.json())
        response.raise_for_status()

    response.raise_for_status()
    return response.text

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="订阅微信公众号")
    parser.add_argument("mp_name", type=str, help="公众号名称")
    args = parser.parse_args()
    
    try:
        print("正在添加公众号...")
        result = add_mp(mp_name=args.mp_name)
        print("添加结果:")
        print(result)
    except Exception as e:
        print(f"请求失败：{e}")
