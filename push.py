"""
push.py - 通过 PushPlus 群组推送消息
文档：https://www.pushplus.plus/doc/guide/api.html
"""
import requests
from config import PUSHPLUS_TOKEN, PUSHPLUS_TOPIC

PUSHPLUS_URL = "http://www.pushplus.plus/send"


def send_message(title: str, content: str) -> bool:
    """
    发送消息到 PushPlus（支持群组推送）
    如果配置了 PUSHPLUS_TOPIC，则推送给群组所有成员
    """
    payload = {
        "token": PUSHPLUS_TOKEN,
        "title": title,
        "content": content,
        "template": "html",
    }
    # 如果有群组编码，加上 topic 参数
    if PUSHPLUS_TOPIC:
        payload["topic"] = PUSHPLUS_TOPIC

    try:
        resp = requests.post(PUSHPLUS_URL, json=payload, timeout=15)
        resp.raise_for_status()
        result = resp.json()
        if result.get("code") == 200:
            target = f"群组({PUSHPLUS_TOPIC})" if PUSHPLUS_TOPIC else "个人"
            print(f"  ✅ 推送成功！→ {target}")
            return True
        else:
            print(f"  ❌ 推送失败：{result.get('msg')}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"  ❌ 网络错误：{e}")
        return False


def build_html_content(
    date_str: str,
    weather_sections: list,
    love_msg: str,
    greeting: str,
) -> str:
    """
    构建包含多城市天气的 HTML 消息

    Args:
        weather_sections: [{"person": "胜泽", "city": "北京", "emoji": "☀️",
                            "text": "晴", "temp_min": "3", "temp_max": "15", "wind": "..."}]
    """
    # 天气区块
    weather_html = ""
    for w in weather_sections:
        weather_html += f"""
    <p style="margin:8px 0; font-size:15px; color:#333;">
        📍 <strong>{w['person']}（{w['city']}）：</strong>
        {w['emoji']} {w['text']} {w['temp_min']}~{w['temp_max']}℃ · {w['wind']}
    </p>"""

    html = f"""
<div style="
    font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif;
    max-width: 480px;
    margin: 0 auto;
    padding: 20px;
    background: linear-gradient(135deg, #fff0f5 0%, #fff5f0 50%, #f0f5ff 100%);
    border-radius: 16px;
    border: 1px solid #ffd6e0;
">
    <!-- 标题 -->
    <div style="text-align:center; margin-bottom:16px;">
        <span style="font-size:28px;">❤️</span>
        <h2 style="color:#e75480; margin:8px 0; font-size:22px; font-weight:bold;">
            今天也是爱你的一天
        </h2>
        <p style="color:#b5495b; font-size:13px; margin:0;">💌 今日特别推送</p>
    </div>

    <hr style="border:none; border-top:1px dashed #ffd6e0; margin:16px 0;">

    <!-- 日期 -->
    <p style="margin:10px 0; font-size:15px; color:#333;">
        📅 <strong>日期：</strong>{date_str}
    </p>

    <!-- 各城市天气 -->
    {weather_html}

    <hr style="border:none; border-top:1px dashed #ffd6e0; margin:16px 0;">

    <!-- 情话 -->
    <div style="
        background:#fff;
        border-radius:12px;
        padding:14px 18px;
        margin:12px 0;
        border-left:4px solid #e75480;
        box-shadow:0 2px 8px rgba(231,84,128,0.08);
    ">
        <p style="margin:0 0 6px 0; font-size:13px; color:#e75480; font-weight:bold;">
            💕 Love Message for You
        </p>
        <p style="
            margin:0; font-size:15px; color:#555;
            line-height:1.7; font-style:italic;
        ">"{love_msg}"</p>
    </div>

    <hr style="border:none; border-top:1px dashed #ffd6e0; margin:16px 0;">

    <!-- 问候 -->
    <p style="text-align:center; font-size:16px; color:#e75480; margin:12px 0; font-weight:bold;">
        {greeting}
    </p>

    <p style="text-align:center; font-size:12px; color:#ccc; margin-top:16px;">
        —— 你专属的每日推送 ——
    </p>
</div>
"""
    return html
