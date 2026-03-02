# 微信每日情话+天气推送 🌸

每天自动向微信推送一条包含**日期、天气、情话**的消息。

---

## 🛠️ 第一步：准备 API Key（都是免费的）

### 1. 获取 PushPlus Token（用于微信推送）
1. 访问 [https://www.pushplus.plus/](https://www.pushplus.plus/)
2. 用微信扫码登录
3. 首页即可看到你的 **Token**，复制下来

### 2. 获取和风天气 API Key（用于获取天气）
1. 访问 [https://dev.qweather.com/](https://dev.qweather.com/) 注册账号
2. 进入控制台 → 应用管理 → 创建应用
3. 复制生成的 **API Key**

---

## ⚙️ 第二步：配置 `.env` 文件

将 `.env.example` 复制一份并重命名为 `.env`：

```bash
copy .env.example .env
```

然后用文本编辑器打开 `.env`，填入你的配置：

```ini
PUSHPLUS_TOKEN=你的pushplus_token
QWEATHER_API_KEY=你的和风天气api_key
LOCATION_ID=101010100    # 你所在城市的ID（见下方城市表）
RECEIVER_NAME=宝贝        # 对TA的称呼
GREETING_MODE=morning    # morning(早安) / evening(晚安) / noon(午安)
```

### 常用城市 Location ID

| 城市 | ID | 城市 | ID |
|---|---|---|---|
| 北京 | 101010100 | 上海 | 101020100 |
| 广州 | 101280101 | 深圳 | 101280601 |
| 杭州 | 101210101 | 南京 | 101190101 |
| 武汉 | 101200101 | 成都 | 101270101 |
| 西安 | 101110101 | 重庆 | 101040100 |
| 天津 | 101030100 | 苏州 | 101190401 |

---

## 📦 第三步：安装依赖

```bash
pip install -r requirements.txt
```

---

## 🚀 第四步：运行

### 立即推送一次（测试用）
```bash
python main.py
```

### 每天定时自动推送（推荐）

#### 方法一：用 Python 脚本持续运行（电脑不关机时有效）
```bash
# 每天早上 7:20 推送
python main.py --schedule 07:20
```

#### 方法二：使用 Windows 任务计划程序（推荐，即使关闭了脚本也能定时启动）
1. 打开"任务计划程序"（开始菜单搜索）
2. 点击"创建基本任务"
3. 触发器选"每天"，设置时间为 07:20
4. 操作选"启动程序"：
   - 程序：`python`
   - 参数：`c:\Users\黄胜泽\Desktop\科研\微信天气\main.py`
   - 起始于：`c:\Users\黄胜泽\Desktop\科研\微信天气`

---

## 📁 文件结构

```
微信天气/
├── .env              # 你的配置文件（不要上传到GitHub！）
├── .env.example      # 配置文件模板
├── requirements.txt  # 依赖包
├── config.py         # 配置读取
├── weather.py        # 天气模块
├── love_message.py   # 情话库（100+条，可自由添加）
├── push.py           # pushplus 推送模块
└── main.py           # 主程序
```

---

## 💕 自定义情话

打开 `love_message.py`，在 `LOVE_MESSAGES` 列表中添加你喜欢的情话即可：

```python
LOVE_MESSAGES = [
    "你新加的情话，",
    "可以加很多条，",
    ...
]
```
