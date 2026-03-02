"""
main.py - PushPlus 群组推送（丰富天气 + Gemini 点评/情话 + 早晚安）

运行方式：
    python main.py               # 早安模式
    python main.py --mode evening # 晚安模式
    python main.py --schedule     # 定时：早上+晚上各推一次
"""
import argparse
import random
import sys
import time
from datetime import date, datetime

import schedule

from config import check_config, CITIES, MORNING_TIME, EVENING_TIME
from weather import get_weather
from love_message import generate_love_message
from push import send_message, build_html_content


GREETINGS = {
    "morning": [
        "🌞 早安啦~~",
        "🌞 早上好，新的一天也要开心哦",
        "☀️ 起床啦，今天也要元气满满！",
        "🌸 早安，愿你今天被温柔对待",
        "💪 新的一天开始了，记得开心",
    ],
    "evening": [
        "🌙 晚安啦~~",
        "🌙 今天辛苦了，早点休息",
        "✨ 晚安，明天也要好好的",
        "🌃 晚安，做个好梦",
        "💫 晚安，月亮替我亲亲你",
    ],
}


def push_once(mode: str = "morning"):
    """执行一次推送"""
    print("=" * 60)
    mode_label = "🌞 早安推送" if mode == "morning" else "🌙 晚安推送"
    print(f"🚀 {mode_label} — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    check_config()
    today = date.today().strftime("%Y-%m-%d")

    # 获取所有城市的天气
    weather_sections = []
    for city in CITIES:
        print(f"\n📍 获取 {city.person}（{city.city_name}）的天气...")
        try:
            w = get_weather(city.city_id)
            print(f"   {w['emoji']} {w['text']} {w['temp_min']}~{w['temp_max']}℃ 体感{w['feels_like']}℃")
            print(f"   💧 湿度{w['humidity']}%  💨 {w['wind_dir']}{w['wind_scale']}级")
            weather_sections.append(w | {"person": city.person, "city": city.city_name})
        except Exception as e:
            print(f"   ⚠️ 获取失败：{e}")
            weather_sections.append({
                "person": city.person, "city": city.city_name,
                "emoji": "🌈", "text": "未知",
                "temp_min": "--", "temp_max": "--",
                "feels_like": "--", "humidity": "--",
                "wind_dir": "--", "wind_scale": "--",
                "wind_speed": "--", "vis": "--", "pressure": "--",
                "sunrise": "--", "sunset": "--", "uv_index": "--",
            })

    # Gemini 生成：天气点评 + 英语情话
    print(f"\n💕 正在请 Gemini 生成...")
    gemini_result = generate_love_message(weather_sections, mode=mode, date_str=today)
    comment = gemini_result["comment"]
    love_msg = gemini_result["love"]

    if comment:
        print(f"\n   📝 天气点评：{comment}")
    print(f"   💌 英语情话：{love_msg}")

    greeting = random.choice(GREETINGS.get(mode, GREETINGS["morning"]))

    # 构建 HTML
    content = build_html_content(
        date_str=today,
        mode=mode,
        weather_sections=weather_sections,
        gemini_comment=comment,
        love_msg=love_msg,
        greeting=greeting,
    )

    # 推送
    title = f"❤️ 今天也是爱你的一天 · {today}"
    send_message(title=title, content=content)

    print(f"\n{'=' * 60}\n")


def run_scheduled():
    print(f"⏰ 定时推送已启动")
    print(f"   🌞 早安：{MORNING_TIME}  🌙 晚安：{EVENING_TIME}")
    print(f"   按 Ctrl+C 停止\n")

    schedule.every().day.at(MORNING_TIME).do(push_once, mode="morning")
    schedule.every().day.at(EVENING_TIME).do(push_once, mode="evening")

    while True:
        schedule.run_pending()
        time.sleep(30)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="微信每日推送")
    parser.add_argument("--schedule", action="store_true", help="启动定时模式")
    parser.add_argument("--mode", choices=["morning", "evening"], default="morning")
    args = parser.parse_args()

    if args.schedule:
        run_scheduled()
    else:
        push_once(mode=args.mode)
