import requests
import os
import json
import math

def fetch_card_and_costume(card_id: int, trained: bool = False) -> tuple:
    """
    获取卡面和服装的信息及图片
    
    Args:
        card_id (int): 卡面编号
        trained (bool): 特训状态，True为特训后，False为特训前
    
    Returns:
        tuple: (card_data, costume_data, card_image, costume_image)
    """
    # 基础URL
    CARD_API_URL = "https://bestdori.com/api/cards/{}.json"
    COSTUME_API_URL = "https://bestdori.com/api/costumes/{}.json"
    
    try:
        # 获取卡面JSON数据
        card_response = requests.get(CARD_API_URL.format(card_id))
        card_data = card_response.json()
        
        # 从卡面数据中获取服装ID
        costume_id = card_data.get('costumeId')
        if costume_id is None:
            raise KeyError("卡面数据中未找到服装ID")
            
        # 获取服装JSON数据
        costume_response = requests.get(COSTUME_API_URL.format(costume_id))
        costume_data = costume_response.json()
        
        # 构建图片URL
        card_image_url = f"https://bestdori.com/assets/cn/characters/resourceset/{card_data['resourceSetName']}_rip/card_{'after_training' if trained else 'normal'}.png"
        costume_group = math.floor(costume_id / 50)
        costume_image_url = f"https://bestdori.com/assets/cn/thumb/costume/group{costume_group}_rip/{costume_data['assetBundleName']}.png"
        
        # 获取图片数据
        card_image = requests.get(card_image_url).content
        costume_image = requests.get(costume_image_url).content
        
        return card_data, costume_data, card_image, costume_image
        
    except requests.RequestException as e:
        print(f"网络请求错误: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"JSON解析错误: {e}")
        return None
    except KeyError as e:
        print(f"数据结构错误: {e}")
        return None
    except Exception as e:
        print(f"未知错误: {e}")
        return None