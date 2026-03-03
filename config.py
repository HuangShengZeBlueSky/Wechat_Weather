"""
config.py - 读取 .env 配置
"""
import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).parent / ".env"
if env_path.exists():
    load_dotenv(env_path)
# 如果 .env 不存在，直接从系统环境变量读取（兼容 GitHub Actions）

# ---- PushPlus ----
PUSHPLUS_TOKEN: str = os.getenv("PUSHPLUS_TOKEN", "")
PUSHPLUS_TOPIC: str = os.getenv("PUSHPLUS_TOPIC", "")

# ---- Gemini ----
GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-3-flash-preview")

# ---- 和风天气 ----
QWEATHER_API_KEY: str = os.getenv("QWEATHER_API_KEY", "")
QWEATHER_API_HOST: str = os.getenv("QWEATHER_API_HOST", "https://devapi.qweather.com")

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
    if not CITIES:
        errors.append("至少需要配置一个城市 (CITY_1_PERSON)")
    if errors:
        raise ValueError(f"❌ 配置不完整：{', '.join(errors)}")
    print(f"✅ 配置加载成功")
    print(f"   PushPlus: {'群组(' + PUSHPLUS_TOPIC + ')' if PUSHPLUS_TOPIC else '仅个人'}")
    print(f"   Gemini: {'✅ ' + GEMINI_MODEL if GEMINI_API_KEY else '❌ 未配置（使用经典情话）'}")
    print(f"   天气: 和风天气 → {QWEATHER_API_HOST}")
    for c in CITIES:
        print(f"   📍 {c.person} — {c.city_name} (ID:{c.city_id})")
