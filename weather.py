"""
weather.py - 从和风天气 API 获取天气信息
支持传入不同城市的 location_id
"""
import requests
from config import QWEATHER_API_KEY

WEATHER_ICON_MAP = {
    "100": ("晴", "☀️"), "101": ("多云", "⛅"), "102": ("少云", "🌤️"),
    "103": ("晴间多云", "🌤️"), "104": ("阴", "☁️"), "150": ("晴", "🌙"),
    "151": ("多云", "🌙"), "300": ("阵雨", "🌦️"), "301": ("强阵雨", "🌧️"),
    "302": ("雷阵雨", "⛈️"), "305": ("小雨", "🌧️"), "306": ("中雨", "🌧️"),
    "307": ("大雨", "🌧️"), "310": ("暴雨", "🌊"), "400": ("小雪", "❄️"),
    "401": ("中雪", "❄️"), "402": ("大雪", "❄️"), "403": ("暴雪", "🌨️"),
    "404": ("雨夹雪", "🌨️"), "500": ("薄雾", "🌫️"), "501": ("雾", "🌫️"),
    "502": ("霾", "😷"), "503": ("扬沙", "💨"), "999": ("未知", "🌈"),
}


def get_weather(location_id: str) -> dict:
    """
    获取指定城市的实时天气 + 今日温度

    Args:
        location_id: 和风天气城市 ID，如 "101010100"

    Returns:
        dict: text, emoji, temp, temp_min, temp_max, wind
    """
    base_url = "https://devapi.qweather.com/v7"
    params = {"location": location_id, "key": QWEATHER_API_KEY}

    # 实时天气
    now_resp = requests.get(f"{base_url}/weather/now", params=params, timeout=10)
    now_resp.raise_for_status()
    now_data = now_resp.json()

    if now_data.get("code") != "200":
        raise RuntimeError(f"和风天气 API 错误：{now_data.get('code')}")

    now = now_data["now"]
    icon_code = now.get("icon", "999")
    text, emoji = WEATHER_ICON_MAP.get(icon_code, (now.get("text", "未知"), "🌈"))

    # 今日温度
    daily_resp = requests.get(f"{base_url}/weather/3d", params=params, timeout=10)
    daily_resp.raise_for_status()
    daily_data = daily_resp.json()

    temp_min, temp_max = now.get("temp", "--"), now.get("temp", "--")
    if daily_data.get("code") == "200" and daily_data.get("daily"):
        today = daily_data["daily"][0]
        temp_min = today.get("tempMin", temp_min)
        temp_max = today.get("tempMax", temp_max)

    wind_dir = now.get("windDir", "")
    wind_scale = now.get("windScale", "")
    wind = f"{wind_dir}{wind_scale}级" if wind_dir else "--"

    return {
        "text": text, "emoji": emoji,
        "temp": now.get("temp", "--"),
        "temp_min": temp_min, "temp_max": temp_max,
        "wind": wind,
    }
