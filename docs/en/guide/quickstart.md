# Quick Start

## Get API Keys

| Service | URL | Notes |
|---|---|---|
| PushPlus | [pushplus.plus](https://www.pushplus.plus/) | Scan WeChat QR to login, copy Token from homepage |
| QWeather | [dev.qweather.com](https://dev.qweather.com/) | Register → Create App → Copy Key + Host |
| Gemini | [aistudio.google.com](https://aistudio.google.com/apikey) | Optional — without it, classic love quotes are used |

## Install

```bash
git clone https://github.com/HuangShengZeBlueSky/Wechat_Weather.git
cd Wechat_Weather
pip install -r requirements.txt
```

## Configure

```bash
copy .env.example .env
```

Edit `.env` with your keys:

```ini
PUSHPLUS_TOKEN=your_token
QWEATHER_API_KEY=your_key
QWEATHER_API_HOST=https://your_host.re.qweatherapi.com
GEMINI_API_KEY=your_gemini_key  # optional
GEMINI_MODEL=gemini-3-flash-preview

CITY_1_PERSON=Alice
CITY_1_ID=101010100
CITY_1_NAME=Beijing
```

## Run

```bash
# Morning push
python main.py --mode morning

# Evening push
python main.py --mode evening

# Scheduled mode (keep running)
python main.py --schedule
```

## Next Steps

- [Architecture](./architecture) — module-by-module breakdown
- [Push Flow](./push-flow) — understand the full push pipeline
- [GitHub Actions](./github-actions) — set up serverless scheduled push
