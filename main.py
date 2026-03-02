"""
main.py - PushPlus 群组推送（多城市天气 + 早安/晚安）

运行方式：
    python main.py               # 立即推送一次（早安模式）
    python main.py --mode evening # 立即推送（晚安模式）
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
    print("=" * 55)
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
            print(f"   {w['emoji']} {w['text']} {w['temp_min']}~{w['temp_max']}℃")
            weather_sections.append({
                "person": city.person,
                "city": city.city_name,
                "emoji": w["emoji"],
                "text": w["text"],
                "temp_min": w["temp_min"],
                "temp_max": w["temp_max"],
                "wind": w["wind"],
            })
        except Exception as e:
            print(f"   ⚠️ 获取失败：{e}")
            weather_sections.append({
                "person": city.person, "city": city.city_name,
                "emoji": "🌈", "text": "未知",
                "temp_min": "--", "temp_max": "--", "wind": "--",
            })

    # Gemini 生成情话（带天气/时间/人名上下文）
    print(f"\n💕 正在用 Gemini 生成情话...")
    love_msg = generate_love_message(weather_sections, mode=mode, date_str=today)
    greeting = random.choice(GREETINGS.get(mode, GREETINGS["morning"]))
    print(f"   {love_msg}")

    # 构建 HTML 消息
    content = build_html_content(
        date_str=today,
        weather_sections=weather_sections,
        love_msg=love_msg,
        greeting=greeting,
    )

    # 推送
    title = f"❤️ 今天也是爱你的一天 · {today}"
    send_message(title=title, content=content)

    print(f"\n{'=' * 55}\n")


def run_scheduled():
    """定时模式"""
    print(f"⏰ 定时推送已启动")
    print(f"   🌞 早安：每天 {MORNING_TIME}")
    print(f"   🌙 晚安：每天 {EVENING_TIME}")
    print(f"   按 Ctrl+C 停止\n")

    schedule.every().day.at(MORNING_TIME).do(push_once, mode="morning")
    schedule.every().day.at(EVENING_TIME).do(push_once, mode="evening")

    while True:
        schedule.run_pending()
        time.sleep(30)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PushPlus 群组每日推送")
    parser.add_argument("--schedule", action="store_true", help="启动定时模式")
    parser.add_argument("--mode", choices=["morning", "evening"], default="morning",
                        help="推送模式（默认 morning）")
    args = parser.parse_args()

    if args.schedule:
        run_scheduled()
    else:
        push_once(mode=args.mode)
