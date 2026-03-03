# Overview

## What Is This?

**WeChat Daily Weather Push** is an automated system that pushes beautifully formatted messages containing **weather info, AI commentary, and love messages** to WeChat every day.

<!-- 📸 Screenshots -->
<!--
![Morning Push](/images/morning_push.png)
-->
::: tip 📸 Screenshots
Place your screenshots in `docs/public/images/`, then uncomment above.
:::

## Features

| Feature | Description |
|---|---|
| 🌤️ Multi-Source Weather | QWeather API (primary) + China Weather (fallback, auto-switch) |
| 🤖 AI-Generated | Gemini generates Chinese commentary + English love messages based on real-time weather |
| 📱 WeChat Push | PushPlus one-to-many push with group support |
| 🏙️ Multi-City | Configure any number of cities, each mapped to a person |
| ⏰ Dual Push | Morning 07:30 + Evening 22:00, auto mode detection |
| ☁️ Serverless | GitHub Actions scheduled run — completely free |

## Data Flow

```
QWeather API ──→ weather.py ──→┐
                               ├──→ main.py ──→ push.py ──→ PushPlus ──→ 📱 WeChat
Gemini API ───→ love_message ──┘
                  .py
```
