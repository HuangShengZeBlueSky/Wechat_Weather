"""
push.py - PushPlus 群组推送（丰富天气 + Gemini 点评 + 情话）
"""
import requests
from config import PUSHPLUS_TOKEN, PUSHPLUS_TOPIC

PUSHPLUS_URL = "http://www.pushplus.plus/send"


def send_message(title: str, content: str) -> bool:
    payload = {
        "token": PUSHPLUS_TOKEN,
        "title": title,
        "content": content,
        "template": "html",
    }
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
    mode: str,
    weather_sections: list,
    gemini_comment: str,
    love_msg: str,
    greeting: str,
) -> str:
    """构建 HTML 推送消息"""

    mode_label = "🌞 早安推送" if mode == "morning" else "🌙 晚安推送"
    mode_color = "#e17055" if mode == "morning" else "#6c5ce7"

    # 天气区块（丰富版）
    weather_html = ""
    for w in weather_sections:
        weather_html += f"""
    <div style="
        background:#fff;
        border-radius:10px;
        padding:12px 16px;
        margin:10px 0;
        box-shadow:0 1px 4px rgba(0,0,0,0.06);
    ">
        <p style="margin:0 0 8px 0; font-size:15px; color:#e75480; font-weight:bold;">
            📍 {w['person']}（{w['city']}）{w['emoji']}
        </p>
        <p style="margin:4px 0; font-size:14px; color:#333;">
            🌡️ {w['text']}　{w['temp_min']}~{w['temp_max']}℃　体感 {w.get('feels_like','--')}℃
        </p>
        <p style="margin:4px 0; font-size:14px; color:#555;">
            💧 湿度 {w.get('humidity','--')}%　　💨 {w.get('wind_dir','--')}{w.get('wind_scale','--')}级
        </p>
        <p style="margin:4px 0; font-size:13px; color:#888;">
            🌅 日出 {w.get('sunrise','--')}　🌇 日落 {w.get('sunset','--')}　☀️ 紫外线 {w.get('uv_index','--')}
        </p>
    </div>"""

    # Gemini 点评
    comment_html = ""
    if gemini_comment:
        comment_html = f"""
    <div style="
        background:#fffbf0;
        border-radius:10px;
        padding:12px 16px;
        margin:12px 0;
        border-left:4px solid #fdcb6e;
    ">
        <p style="margin:0 0 4px 0; font-size:13px; color:#e17055; font-weight:bold;">🤖 Gemini 说</p>
        <p style="margin:0; font-size:14px; color:#555; line-height:1.7;">{gemini_comment}</p>
    </div>"""

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
        <p style="color:{mode_color}; font-size:14px; margin:0; font-weight:bold;">
            {mode_label}
        </p>
    </div>

    <hr style="border:none; border-top:1px dashed #ffd6e0; margin:16px 0;">

    <!-- 日期 -->
    <p style="margin:10px 0; font-size:15px; color:#333;">
        📅 <strong>{date_str}</strong>
    </p>

    <!-- 各城市详细天气 -->
    {weather_html}

    {comment_html}

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
        <p style="margin:0; font-size:15px; color:#555; line-height:1.8; font-style:italic;">
            "{love_msg}"
        </p>
    </div>

    <hr style="border:none; border-top:1px dashed #ffd6e0; margin:16px 0;">

    <!-- 问候 -->
    <p style="text-align:center; font-size:16px; color:{mode_color}; margin:12px 0; font-weight:bold;">
        {greeting}
    </p>

    <p style="text-align:center; font-size:12px; color:#ccc; margin-top:16px;">
        —— 你专属的每日推送 ——
    </p>
</div>
"""
    return html
