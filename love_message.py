"""
love_message.py - 使用 Gemini 生成：天气点评 + 个性化英语情话
"""
import random
from datetime import datetime

from google import genai
from config import GEMINI_API_KEY, GEMINI_MODEL

CLASSIC_LOVE_MESSAGES = [
    "You are my today and all of my tomorrows.",
    "In a sea of people, my eyes will always search for you.",
    "Every love story is beautiful, but ours is my favorite.",
    "I fell in love the way you fall asleep: slowly, and then all at once.",
    "You are my sun, my moon, and all my stars.",
    "If I had a flower for every time I thought of you, I could walk through my garden forever.",
    "My heart is and always will be yours.",
    "You are my greatest adventure.",
    "I love you to the moon and back.",
    "Wherever you are is my home.",
    "I choose you. And I'll choose you over and over.",
    "If I know what love is, it is because of you.",
    "You are the poem I never knew how to write.",
    "I'd choose you in a hundred lifetimes, in any version of reality.",
    "My favorite place in the world is next to you.",
    "I love you more than yesterday, less than tomorrow.",
]


def generate_love_message(
    weather_sections: list,
    mode: str = "morning",
    date_str: str = "",
) -> dict:
    """
    使用 Gemini 生成：天气点评 + 英语情话

    Returns:
        dict: {"comment": "天气点评...", "love": "英语情话..."}
    """
    if not GEMINI_API_KEY:
        return {
            "comment": "",
            "love": random.choice(CLASSIC_LOVE_MESSAGES),
        }

    time_label = "早上 (morning)" if mode == "morning" else "晚上 (evening)"
    weather_desc = "\n".join(
        f"- {w['person']} 在 {w['city']}：{w['text']} {w.get('temp_min','--')}~{w.get('temp_max','--')}℃, "
        f"体感{w.get('feels_like','--')}℃, 湿度{w.get('humidity','--')}%, "
        f"风{w.get('wind_dir','--')}{w.get('wind_scale','--')}级"
        for w in weather_sections
    )
    inspirations = random.sample(CLASSIC_LOVE_MESSAGES, 3)
    inspiration_text = "\n".join(f"  - {m}" for m in inspirations)

    prompt = f"""You are writing a daily message for a couple: 黄胜泽 (Shengze, in Beijing) and 马一心 (Yixin, in Nanchang).

Today's info:
- Date: {date_str or datetime.now().strftime('%Y-%m-%d')}
- Time of day: {time_label}
- Weather:
{weather_desc}

Please write TWO parts, clearly labeled:

**PART 1 - Weather Commentary (in Chinese, 2-3 sentences):**
Based on the weather above, give a warm, caring comment. For example, if it's cold remind them to dress warm, if it's rainy remind them to bring an umbrella, if it's sunny encourage them to enjoy the day. Be specific to the actual weather data. Address both 胜泽 and 一心 by name if their weather is different.

**PART 2 - Love Message (in English, 2-3 sentences):**
Write a sweet, poetic English love message. Naturally weave in the weather or time of day. Make it feel personal to Shengze and Yixin. Be creative and different each time.

Style inspirations for Part 2 (do NOT copy these):
{inspiration_text}

Format your response EXACTLY like this (keep the labels):
COMMENT: [your Chinese weather commentary here]
LOVE: [your English love message here]"""

    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
            config={
                "temperature": 0.85,
                "max_output_tokens": 1024,
            },
        )
        text = response.text.strip()

        # 解析 COMMENT 和 LOVE
        comment = ""
        love = ""
        if "COMMENT:" in text and "LOVE:" in text:
            parts = text.split("LOVE:")
            comment = parts[0].replace("COMMENT:", "").strip()
            love = parts[1].strip().strip('"').strip("'").strip()
        else:
            # 如果格式不对，整段作为 love
            love = text.strip('"').strip("'").strip()

        return {
            "comment": comment if comment else "",
            "love": love if love else random.choice(CLASSIC_LOVE_MESSAGES),
        }
    except Exception as e:
        print(f"  ⚠️ Gemini 调用失败（{e}），使用经典情话")
        return {
            "comment": "",
            "love": random.choice(CLASSIC_LOVE_MESSAGES),
        }


if __name__ == "__main__":
    test_sections = [
        {"person": "胜泽", "city": "北京", "text": "阴", "temp_min": "0", "temp_max": "5",
         "feels_like": "-2", "humidity": "40", "wind_dir": "北风", "wind_scale": "3"},
        {"person": "一心", "city": "南昌", "text": "阴", "temp_min": "9", "temp_max": "14",
         "feels_like": "7", "humidity": "75", "wind_dir": "东风", "wind_scale": "2"},
    ]
    result = generate_love_message(test_sections, mode="morning")
    print(f"📝 点评：{result['comment']}")
    print(f"💕 情话：{result['love']}")
