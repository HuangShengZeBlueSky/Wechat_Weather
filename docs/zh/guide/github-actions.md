# GitHub Actions 配置

## 工作流文件

工作流定义在 `.github/workflows/schedule.yml`，包含两个定时触发 + 手动触发。

## 配置 Secrets

进入仓库 → **Settings** → **Secrets and variables** → **Actions** → **New repository secret**

需要配置的 Secrets：

| Name | 说明 | 必须 |
|---|---|---|
| `PUSHPLUS_TOKEN` | PushPlus 推送 Token | ✅ |
| `PUSHPLUS_TOPIC` | 群组编码 | ❌ 可选 |
| `GEMINI_API_KEY` | Gemini API Key | ❌ 不配则用经典情话 |
| `GEMINI_MODEL` | 模型名称 | ❌ 默认 `gemini-3-flash-preview` |
| `QWEATHER_API_KEY` | 和风天气 Key | ✅ |
| `QWEATHER_API_HOST` | 和风天气 Host | ✅ |

::: warning ⚠️ 命名必须完全一致
Secret 的 Name **必须**和表格中完全一样（大写、下划线），否则代码读不到。
:::

<!-- 📸 Secrets 配置截图 -->
<!--
![Secrets 配置页面](/images/secrets_config.png)
-->
::: tip 📸 Secrets 配置截图
放入 `docs/public/images/secrets_config.png`
:::

## 城市配置

城市信息不是敏感数据，直接写在 `schedule.yml` 中：

```yaml
env:
  CITY_1_PERSON: 胜泽
  CITY_1_ID: '101010100'
  CITY_1_NAME: 北京
  CITY_2_PERSON: 一心
  CITY_2_ID: '101240101'
  CITY_2_NAME: 南昌
```

如需修改城市，直接编辑此文件并推送。

## 手动触发测试

1. 进入 **Actions** → **Daily Weather Push**
2. 点击 **Run workflow**
3. 选择模式 → 运行

<!-- 📸 手动触发截图 -->
<!--
![手动触发](/images/manual_trigger.png)
-->
::: tip 📸 手动触发截图
放入 `docs/public/images/manual_trigger.png`
:::

## 查看运行日志

点击运行记录 → **run-script** → 展开查看每一步的输出。

常见问题：

| 问题 | 排查 |
|---|---|
| `配置不完整：PUSHPLUS_TOKEN` | Secret 未配置或名称拼写错误 |
| `至少需要配置一个城市` | `CITY_1_PERSON` 未配置 |
| 天气获取失败 | 检查 `QWEATHER_API_KEY` 和 `QWEATHER_API_HOST` |
| Gemini 调用失败 | 检查 `GEMINI_API_KEY` 是否有效 |
| 定时没触发 | 延迟 5~15 分钟是正常的 |

## 免费额度

- 公开仓库：**无限制**
- 私有仓库：每月 **2000 分钟**
- 此脚本每次运行约 1~2 分钟，一天两次 = 每月约 60 分钟，**完全够用**
