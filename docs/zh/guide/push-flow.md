# 推送流程

## 三种推送方式对比

| 方式 | 触发者 | 环境 | 适用场景 |
|---|---|---|---|
| 本地手动 | 你自己在终端 | 本地电脑 | 开发测试 |
| GitHub 手动 | 你在 Actions 页面点击 | GitHub 服务器 | 远程测试 |
| GitHub 定时 | GitHub cron 自动 | GitHub 服务器 | **日常使用** |

---

## 方式一：本地手动运行

```bash
python main.py --mode morning
```

```
你的电脑
  │
  ├─ 读取 .env 配置
  ├─ 调用和风天气 API → 获取天气
  ├─ 调用 Gemini API → 生成点评 + 情话
  ├─ 构建 HTML 卡片
  └─ 调用 PushPlus API → 微信收到推送 📱
```

<!-- 📸 终端运行截图 -->
<!--
![本地运行](/images/local_run.png)
-->
::: tip 📸 本地运行截图
放入 `docs/public/images/local_run.png`
:::

---

## 方式二：GitHub Actions 手动触发

1. 进入仓库 → **Actions** → **Daily Weather Push**
2. 点击 **Run workflow**
3. 选择推送模式 → 点击运行

<!-- 📸 手动触发截图 -->
<!--
![GitHub Actions 手动触发](/images/actions_manual.png)
-->
::: tip 📸 手动触发截图
放入 `docs/public/images/actions_manual.png`
:::

```
GitHub 服务器
  │
  ├─ 分配全新 Ubuntu 虚拟机
  ├─ git clone 你的代码
  ├─ 安装 Python 3.10 + 依赖
  ├─ 从 Secrets 注入环境变量
  ├─ python main.py --mode <你选的模式>
  │    ├─ 和风天气 API → 天气
  │    ├─ Gemini API → 情话
  │    └─ PushPlus API → 微信推送 📱
  └─ 销毁虚拟机
```

---

## 方式三：GitHub Actions 定时触发

这是**推荐的日常使用方式**。代码推上去后全自动运行，无需操心。

### 时间表

| Cron (UTC) | 北京时间 | 模式 |
|---|---|---|
| `30 23 * * *` | 每天 07:30 | 🌞 早安 morning |
| `0 14 * * *` | 每天 22:00 | 🌙 晚安 evening |

### 完整运行过程

```
[UTC 23:30] GitHub 调度系统检查 cron 
  ↓
分配全新 Ubuntu 虚拟机 (~10s)
  ↓
Step 1: actions/checkout@v4 — 拉取代码 (~3s)
  ↓
Step 2: actions/setup-python@v5 — 安装 Python 3.10 (~15s)
  ↓
Step 3: pip install -r requirements.txt — 安装依赖 (~20s)
  ↓
Step 4: 判断推送模式 — UTC 23点 → morning (~1s)
  ↓
Step 5: 注入 Secrets 为环境变量 + 执行 python main.py (~30s)
  ↓
销毁虚拟机 — 每次都是全新环境，无状态
```

::: warning ⏱️ 关于延迟
GitHub Actions 的 cron 触发有 **5~15 分钟的延迟**，这是 GitHub 的已知限制。实际推送时间可能在 07:30~07:45 之间。
:::

### 运行日志

每次运行后可在 **Actions** 页面查看详细日志：

<!-- 📸 运行日志截图 -->
<!--
![Actions 运行日志](/images/actions_log.png)
-->
::: tip 📸 运行日志截图
放入 `docs/public/images/actions_log.png`
:::

---

## 推送消息最终效果

所有方式最终产出的消息格式相同：

```
┌──────────────────────────────────┐
│         ❤️ 今天也是爱你的一天      │
│         🌞 早安推送               │
│──────────────────────────────────│
│ 📅 2026-03-03                    │
│                                  │
│ 📍 胜泽（北京）☀️                │
│ 🌡️ 晴  2~12℃  体感 5℃          │
│ 💧 湿度 30%  💨 北风3级           │
│ 🌅 日出 06:38  🌇 日落 18:10     │
│                                  │
│ 📍 一心（南昌）🌧️                │
│ 🌡️ 小雨  8~14℃  体感 6℃        │
│ 💧 湿度 85%  💨 东风2级           │
│                                  │
│ 🤖 Gemini 说                     │
│ 北京今天晴朗但温差大...           │
│                                  │
│ 💕 Love Message for You          │
│ "Like the morning sun..."        │
│                                  │
│ 🌞 早安啦~~                      │
└──────────────────────────────────┘
```

<!-- 📸 微信收到的推送截图 -->
<!--
![微信推送效果](/images/wechat_push.png)
-->
::: tip 📸 微信推送效果截图
放入 `docs/public/images/wechat_push.png`
:::
