"""
config.py - 读取 .env 配置，PushPlus 群组推送 + 多城市天气
"""
import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).parent / ".env"
if not env_path.exists():
    raise FileNotFoundError("未找到 .env 文件！请将 .env.example 复制为 .env 并填入你的配置。")

load_dotenv(env_path)

# ---- PushPlus ----
PUSHPLUS_TOKEN: str = os.getenv("PUSHPLUS_TOKEN", "")
PUSHPLUS_TOPIC: str = os.getenv("PUSHPLUS_TOPIC", "")  # 群组编码

# ---- 和风天气 ----
QWEATHER_API_KEY: str = os.getenv("QWEATHER_API_KEY", "")

# ---- 推送时间 ----
MORNING_TIME: str = os.getenv("MORNING_TIME", "07:20")
EVENING_TIME: str = os.getenv("EVENING_TIME", "22:00")


# ---- 多城市配置 ----
class CityConfig:
    def __init__(self, person: str, city_id: str, city_name: str):
        self.person = person
        self.city_id = city_id
        self.city_name = city_name

    def __repr__(self):
        return f"{self.person}({self.city_name})"


def load_cities() -> list:
    """自动加载 CITY_N_ 前缀的城市配置"""
    cities = []
    for i in range(1, 20):
        person = os.getenv(f"CITY_{i}_PERSON")
        if person is None:
            break
        city_id = os.getenv(f"CITY_{i}_ID", "101010100")
        city_name = os.getenv(f"CITY_{i}_NAME", "未知")
        cities.append(CityConfig(person=person, city_id=city_id, city_name=city_name))
    return cities


CITIES = load_cities()


def check_config():
    errors = []
    if not PUSHPLUS_TOKEN or "你的" in PUSHPLUS_TOKEN:
        errors.append("PUSHPLUS_TOKEN")
    if not QWEATHER_API_KEY or "你的" in QWEATHER_API_KEY:
        errors.append("QWEATHER_API_KEY")
    if not CITIES:
        errors.append("至少需要配置一个城市 (CITY_1_PERSON)")
    if errors:
        raise ValueError(f"❌ 配置不完整：{', '.join(errors)}")
    print(f"✅ 配置加载成功")
    print(f"   群组：{'已配置 (' + PUSHPLUS_TOPIC + ')' if PUSHPLUS_TOPIC else '未配置（仅推送给自己）'}")
    for c in CITIES:
        print(f"   📍 {c.person} — {c.city_name} (ID:{c.city_id})")
