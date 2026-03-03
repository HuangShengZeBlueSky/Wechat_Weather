# 快速开始

## 准备 API Key

| 服务 | 获取地址 | 说明 |
|---|---|---|
| PushPlus | [pushplus.plus](https://www.pushplus.plus/) | 微信扫码登录，首页复制 Token |
| 和风天气 | [dev.qweather.com](https://dev.qweather.com/) | 注册 → 创建应用 → 复制 Key + Host |
| Gemini | [aistudio.google.com](https://aistudio.google.com/apikey) | 可选，不配置则使用内置经典情话库 |

## 安装

```bash
# 克隆仓库
git clone https://github.com/HuangShengZeBlueSky/Wechat_Weather.git
cd Wechat_Weather

# 安装 Python 依赖
pip install -r requirements.txt
```

## 配置

```bash
# 复制配置模板
copy .env.example .env
```

编辑 `.env` 文件，填入你的 API Key 和城市配置：

```ini
# PushPlus
PUSHPLUS_TOKEN=你的token

# 和风天气
QWEATHER_API_KEY=你的key
QWEATHER_API_HOST=https://你的host.re.qweatherapi.com

# Gemini（可选）
GEMINI_API_KEY=你的gemini_key
GEMINI_MODEL=gemini-3-flash-preview

# 城市配置
CITY_1_PERSON=胜泽
CITY_1_ID=101010100
CITY_1_NAME=北京

CITY_2_PERSON=一心
CITY_2_ID=101240101
CITY_2_NAME=南昌
```

::: tip 城市 ID 查询
常用城市：北京 `101010100`、上海 `101020100`、广州 `101280101`、深圳 `101280601`、南昌 `101240101`

完整列表：[QWeather LocationList](https://github.com/qwd/LocationList)
:::

## 运行

```bash
# 早安推送
python main.py --mode morning

# 晚安推送
python main.py --mode evening

# 定时模式（保持运行）
python main.py --schedule
```

![终端运行效果](/images/terminal_run.png)

## 下一步

- [代码架构](./architecture) — 了解每个模块的职责
- [推送流程](./push-flow) — 了解完整的推送流程
- [GitHub Actions](./github-actions) — 配置免服务器定时推送
