"""
love_message.py - 使用 Gemini 生成个性化英语情话
基于天气、时间、城市、人名（黄胜泽 & 马一心）生成
"""
import random
from datetime import datetime

import google.generativeai as genai
from config import GEMINI_API_KEY, GEMINI_MODEL

# 经典英语情话（Gemini 不可用时的备用 + 风格参考）
CLASSIC_LOVE_MESSAGES = [
    "You are my today and all of my tomorrows.",
    "In a sea of people, my eyes will always search for you.",
    "I love you not only for what you are, but for what I am when I'm with you.",
    "Every love story is beautiful, but ours is my favorite.",
    "I fell in love the way you fall asleep: slowly, and then all at once.",
    "You are my sun, my moon, and all my stars.",
    "If I had a flower for every time I thought of you, I could walk through my garden forever.",
    "My heart is and always will be yours.",
    "You are my greatest adventure.",
    "I love you to the moon and back.",
    "Together is my favorite place to be.",
    "Wherever you are is my home.",
    "I choose you. And I'll choose you over and over.",
    "If I know what love is, it is because of you.",
    "You are the poem I never knew how to write.",
    "I'd choose you in a hundred lifetimes, in any version of reality.",
    "My favorite place in the world is next to you.",
    "I love you more than yesterday, less than tomorrow.",
    "You stole my heart, but I'll let you keep it.",
    "I look at you and see the rest of my life in front of my eyes.",
]


def generate_love_message(
    weather_sections: list,
    mode: str = "morning",
    date_str: str = "",
) -> str:
    """
    使用 Gemini 生成个性化英语情话

    Args:
        weather_sections: [{"person":"胜泽","city":"北京","text":"晴","temp_min":"3","temp_max":"15"}]
        mode: "morning" / "evening"
        date_str: 日期字符串

    Returns:
        str: 英语情话
    """
    if not GEMINI_API_KEY:
        return random.choice(CLASSIC_LOVE_MESSAGES)

    # 构建上下文
    time_context = "morning (early day)" if mode == "morning" else "evening (night time)"
    weather_desc = "; ".join(
        f"{w['person']} is in {w['city']}, weather: {w['text']} {w.get('temp_min','--')}~{w.get('temp_max','--')}℃"
        for w in weather_sections
    )
    inspirations = random.sample(CLASSIC_LOVE_MESSAGES, 3)
    inspiration_text = "\n".join(f"- {m}" for m in inspirations)

    prompt = f"""You are a romantic poet writing a short love message for a couple: 黄胜泽 (Shengze) and 马一心 (Yixin).

Context:
- Date: {date_str or datetime.now().strftime('%Y-%m-%d')}
- Time: {time_context}
- {weather_desc}

Style inspirations (for reference only, do NOT copy):
{inspiration_text}

Write ONE short, sweet, creative English love message (1-2 sentences max).
Requirements:
- Must be in English
- Naturally weave in the weather or time of day when it fits
- Make it feel personal and warm, occasionally use their names (Shengze or Yixin)
- Be poetic but not overly flowery
- Different from the inspirations above
- Do NOT include quotes around the message
- Do NOT include any explanation, just the message itself"""

    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel(GEMINI_MODEL)
        response = model.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(
                temperature=0.9,
                max_output_tokens=100,
            ),
        )
        text = response.text.strip().strip('"').strip("'").strip()
        if text:
            return text
    except Exception as e:
        print(f"  ⚠️ Gemini 调用失败（{e}），使用经典情话")

    return random.choice(CLASSIC_LOVE_MESSAGES)


def get_random_love_message() -> str:
    """备用：随机返回经典情话"""
    return random.choice(CLASSIC_LOVE_MESSAGES)


if __name__ == "__main__":
    test_sections = [
        {"person": "胜泽", "city": "北京", "text": "晴", "temp_min": "3", "temp_max": "15"},
        {"person": "一心", "city": "南昌", "text": "多云", "temp_min": "8", "temp_max": "18"},
    ]
    msg = generate_love_message(test_sections, mode="morning")
    print(f"💕 {msg}")
