# Architecture

## Project Structure

```
Wechat_Weather/
├── main.py               # 🚀 Entry: CLI + push scheduling
├── config.py             # ⚙️ Config: reads .env or env vars
├── weather.py            # 🌤️ Weather: QWeather + China Weather fallback
├── love_message.py       # 💕 AI: Gemini love message generation
├── push.py               # 📤 Push: HTML builder + PushPlus delivery
├── .github/workflows/
│   └── schedule.yml      # ⏰ GitHub Actions scheduled workflow
├── .env                  # 🔒 Local config (gitignored)
├── .env.example          # 📋 Config template
└── requirements.txt      # 📦 Dependencies
```

## Module Details

### `config.py` — Config Center

- `.env` file is **optional** — works both locally and on GitHub Actions
- Dynamically loads cities via `CITY_1_*`, `CITY_2_*`, ... naming pattern

### `weather.py` — Weather Data

```
Request flow:
  QWeather API ──success──→ Return rich data
       │
       └── fail ──→ China Weather (fallback) ──success──→ Return basic data
                         │
                         └── fail ──→ Raise exception
```

Returns: temp, feels-like, humidity, wind, sunrise/sunset, UV index.

### `love_message.py` — AI Love Messages

- **Gemini available** → builds prompt with weather + names + mode → calls Gemini → parses COMMENT + LOVE
- **No Gemini** → randomly picks from 16 classic English love quotes

### `push.py` — Message Delivery

- `build_html_content()` — builds a beautiful HTML card
- `send_message()` — calls PushPlus API (supports personal + group push)

### `main.py` — Entry Point

```
python main.py
   ├── --mode morning    → push_once("morning")
   ├── --mode evening    → push_once("evening")
   └── --schedule        → register two timers, run continuously
```
