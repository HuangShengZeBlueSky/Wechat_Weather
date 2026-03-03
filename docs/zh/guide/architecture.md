# 代码架构

## 整体结构

```
微信天气/
├── main.py               # 🚀 入口：CLI 解析 + 推送调度
├── config.py             # ⚙️ 配置：读取 .env 或环境变量
├── weather.py            # 🌤️ 天气：和风 API + 中国天气网备用
├── love_message.py       # 💕 情话：Gemini AI 生成
├── push.py               # 📤 推送：HTML 构建 + PushPlus 发送
├── .github/workflows/
│   └── schedule.yml      # ⏰ GitHub Actions 定时任务
├── .env                  # 🔒 本地配置（不上传 GitHub）
├── .env.example          # 📋 配置模板
└── requirements.txt      # 📦 依赖
```

## 模块详解

### `config.py` — 配置中心

```python
# 核心逻辑：
env_path = Path(__file__).parent / ".env"
if env_path.exists():
    load_dotenv(env_path)    # 本地：从 .env 加载
# GitHub Actions：直接从系统环境变量读取

# 动态加载多城市配置（CITY_1_*, CITY_2_*, ...）
CITIES = load_cities()
```

**设计要点**：
- `.env` 文件**可选**，同时兼容本地运行和 GitHub Actions
- 城市数量不限，按 `CITY_1_`、`CITY_2_` ... 的命名规则自动识别

---

### `weather.py` — 天气数据获取

```
请求流程：
  和风天气 API ──成功──→ 返回丰富数据
       │
       └── 失败 ──→ 中国天气网（备用）──成功──→ 返回基础数据
                          │
                          └── 失败 ──→ 抛出异常
```

和风天气返回的数据字段：

| 字段 | 说明 |
|---|---|
| `text` / `emoji` | 天气描述 + 对应 emoji |
| `temp_min` / `temp_max` | 最低/最高温度 |
| `feels_like` | 体感温度 |
| `humidity` | 湿度 |
| `wind_dir` / `wind_scale` | 风向 + 风力等级 |
| `sunrise` / `sunset` | 日出/日落时间 |
| `uv_index` | 紫外线指数 |

---

### `love_message.py` — AI 情话生成

```
Gemini 可用？
   ├── 是 → 构建 Prompt（天气 + 人名 + 模式）→ 调用 Gemini
   │        → 解析返回的 COMMENT + LOVE 两部分
   └── 否 → 从 16 条经典英语情话中随机选取
```

**Prompt 设计**：告诉 Gemini 两人的名字、所在城市、当天天气，让它：
1. 生成**中文天气点评**（2-3 句，针对性关怀）
2. 生成**英语情话**（2-3 句，融入天气元素）

---

### `push.py` — 消息推送

- `build_html_content()` — 构建精美 HTML 卡片
- `send_message()` — 调用 PushPlus API 推送

支持**个人推送**和**群组推送**（通过 `PUSHPLUS_TOPIC` 配置）。

---

### `main.py` — 入口调度

```
python main.py
   ├── --mode morning    → push_once("morning")
   ├── --mode evening    → push_once("evening")
   └── --schedule        → 注册两个定时任务，持续运行
                             ├── 每天 MORNING_TIME → morning
                             └── 每天 EVENING_TIME → evening
```

<!-- 📸 架构图 -->
<!--
![系统架构图](/images/architecture.png)
-->
::: tip 📸 架构图
如果你有更精美的架构图，放入 `docs/public/images/architecture.png`
:::
