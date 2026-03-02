"""
weather.py - 天气信息获取（丰富数据版）
优先和风天气（含体感温度、湿度、能见度、紫外线等），失败用中国天气网备用
"""
import requests
from config import QWEATHER_API_KEY, QWEATHER_API_HOST

WEATHER_EMOJI = {
    "晴": "☀️", "多云": "⛅", "阴": "☁️", "少云": "🌤️", "晴间多云": "🌤️",
    "小雨": "🌧️", "中雨": "🌧️", "大雨": "🌧️", "暴雨": "🌊",
    "阵雨": "🌦️", "雷阵雨": "⛈️",
    "雨夹雪": "🌨️", "小雪": "❄️", "中雪": "❄️", "大雪": "❄️", "暴雪": "🌨️",
    "雾": "🌫️", "薄雾": "🌫️", "霾": "😷", "扬沙": "💨",
}


def _get_weather_qweather(city_id: str) -> dict:
    """和风天气 API（丰富数据）"""
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

    # 3天预报
    daily_resp = requests.get(f"{base_url}/weather/3d", params=params, timeout=10)
    daily_resp.raise_for_status()
    daily_data = daily_resp.json()

    temp_min, temp_max = now.get("temp", "--"), now.get("temp", "--")
    sunrise, sunset = "--", "--"
    uv_index = "--"
    if daily_data.get("code") == "200" and daily_data.get("daily"):
        today = daily_data["daily"][0]
        temp_min = today.get("tempMin", temp_min)
        temp_max = today.get("tempMax", temp_max)
        sunrise = today.get("sunrise", "--")
        sunset = today.get("sunset", "--")
        uv_index = today.get("uvIndex", "--")

    return {
        "text": weather_text,
        "emoji": emoji,
        "temp": now.get("temp", "--"),
        "temp_min": temp_min,
        "temp_max": temp_max,
        "feels_like": now.get("feelsLike", "--"),
        "humidity": now.get("humidity", "--"),
        "wind_dir": now.get("windDir", "--"),
        "wind_scale": now.get("windScale", "--"),
        "wind_speed": now.get("windSpeed", "--"),
        "vis": now.get("vis", "--"),
        "pressure": now.get("pressure", "--"),
        "sunrise": sunrise,
        "sunset": sunset,
        "uv_index": uv_index,
        "source": "和风天气",
    }


def _get_weather_china(city_id: str) -> dict:
    """中国天气网（备用）"""
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
    fl = today.get("fl", "").replace("<![CDATA[", "").replace("]]>", "")

    return {
        "text": weather_type,
        "emoji": WEATHER_EMOJI.get(weather_type, "🌈"),
        "temp": info.get("wendu", "--"),
        "temp_min": low,
        "temp_max": high,
        "feels_like": "--",
        "humidity": info.get("shidu", "--"),
        "wind_dir": fx,
        "wind_scale": fl,
        "wind_speed": "--",
        "vis": "--",
        "pressure": "--",
        "sunrise": "--",
        "sunset": "--",
        "uv_index": "--",
        "source": "中国天气网",
    }


def get_weather(city_id: str) -> dict:
    """获取天气：优先和风，失败用中国天气网"""
    try:
        return _get_weather_qweather(city_id)
    except Exception as e:
        print(f"   ⚠️ 和风天气失败（{e}），切换到备用...")
    try:
        return _get_weather_china(city_id)
    except Exception as e2:
        raise RuntimeError(f"所有天气源均失败：{e}, {e2}")
