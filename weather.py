"""
weather.py - 天气信息获取
优先使用和风天气 API（用户专属 host），失败则用中国天气网备用
"""
import requests
from config import QWEATHER_API_KEY, QWEATHER_API_HOST

# 天气 → emoji
WEATHER_EMOJI = {
    "晴": "☀️", "多云": "⛅", "阴": "☁️", "少云": "🌤️", "晴间多云": "🌤️",
    "小雨": "🌧️", "中雨": "🌧️", "大雨": "🌧️", "暴雨": "🌊",
    "阵雨": "🌦️", "雷阵雨": "⛈️",
    "雨夹雪": "🌨️", "小雪": "❄️", "中雪": "❄️", "大雪": "❄️", "暴雪": "🌨️",
    "雾": "🌫️", "薄雾": "🌫️", "霾": "😷", "扬沙": "💨",
}


def _get_weather_qweather(city_id: str) -> dict:
    """和风天气 API（用户专属 host）"""
    base_url = f"{QWEATHER_API_HOST}/v7"
    params = {"location": city_id, "key": QWEATHER_API_KEY}

    # 实时天气
    now_resp = requests.get(f"{base_url}/weather/now", params=params, timeout=10)
    now_resp.raise_for_status()
    now_data = now_resp.json()

    if now_data.get("code") != "200":
        raise RuntimeError(f"和风 code={now_data.get('code')}")

    now = now_data["now"]
    weather_text = now.get("text", "未知")
    emoji = WEATHER_EMOJI.get(weather_text, "🌈")

    # 3天预报（获取今日最低/最高温）
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

    return {
        "text": weather_text,
        "emoji": emoji,
        "temp": now.get("temp", "--"),
        "temp_min": temp_min,
        "temp_max": temp_max,
        "wind": f"{wind_dir}{wind_scale}级" if wind_dir else "--",
        "humidity": now.get("humidity", "--"),
    }


def _get_weather_china(city_id: str) -> dict:
    """中国天气网（备用，免费无需 Key）"""
    url = f"http://t.weather.itboy.net/api/weather/city/{city_id}"
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    resp.encoding = "utf-8"
    data = resp.json()

    if data.get("status") != 200:
        raise RuntimeError(f"天气网 status={data.get('status')}")

    info = data.get("data", {})
    forecast = info.get("forecast", [{}])
    today = forecast[0] if forecast else {}

    weather_type = today.get("type", "未知")
    high = today.get("high", "--").replace("高温 ", "").replace("℃", "")
    low = today.get("low", "--").replace("低温 ", "").replace("℃", "")
    fx = today.get("fx", "")
    fl = today.get("fl", "")

    return {
        "text": weather_type,
        "emoji": WEATHER_EMOJI.get(weather_type, "🌈"),
        "temp": info.get("wendu", "--"),
        "temp_min": low,
        "temp_max": high,
        "wind": f"{fx}{fl}" if fx else "--",
        "humidity": info.get("shidu", "--"),
    }


def get_weather(city_id: str) -> dict:
    """
    获取天气：优先和风天气，失败则用中国天气网

    Returns:
        dict: text, emoji, temp, temp_min, temp_max, wind, humidity
    """
    # 优先：和风天气
    try:
        result = _get_weather_qweather(city_id)
        result["source"] = "和风天气"
        return result
    except Exception as e:
        print(f"   ⚠️ 和风天气失败（{e}），切换到中国天气网...")

    # 备用：中国天气网
    try:
        result = _get_weather_china(city_id)
        result["source"] = "中国天气网"
        return result
    except Exception as e2:
        raise RuntimeError(f"所有天气源均失败：和风({e})，天气网({e2})")


if __name__ == "__main__":
    for name, cid in [("北京", "101010100"), ("南昌", "101240101")]:
        try:
            w = get_weather(cid)
            print(f"{name}: {w['emoji']} {w['text']} {w['temp_min']}~{w['temp_max']}℃ ({w['source']})")
        except Exception as e:
            print(f"{name}: 错误 - {e}")
