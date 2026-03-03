# GitHub Actions Setup

## Workflow File

The workflow is defined in `.github/workflows/schedule.yml` with dual cron triggers + manual dispatch.

## Configure Secrets

Go to repo → **Settings** → **Secrets and variables** → **Actions** → **New repository secret**

| Name | Description | Required |
|---|---|---|
| `PUSHPLUS_TOKEN` | PushPlus push token | ✅ |
| `PUSHPLUS_TOPIC` | Group code | ❌ Optional |
| `GEMINI_API_KEY` | Gemini API Key | ❌ Classic quotes used if empty |
| `GEMINI_MODEL` | Model name | ❌ Default: `gemini-3-flash-preview` |
| `QWEATHER_API_KEY` | QWeather API Key | ✅ |
| `QWEATHER_API_HOST` | QWeather Host | ✅ |

::: warning ⚠️ Names must match exactly
Secret names are case-sensitive and must match the table above exactly.
:::

## City Config

City info is not sensitive — it's hardcoded directly in `schedule.yml`:

```yaml
env:
  CITY_1_PERSON: Alice
  CITY_1_ID: '101010100'
  CITY_1_NAME: Beijing
```

## Manual Trigger Test

1. **Actions** → **Daily Weather Push** → **Run workflow**
2. Select mode → Run
3. Check logs for success/failure

## Troubleshooting

| Issue | Fix |
|---|---|
| `PUSHPLUS_TOKEN` missing | Add Secret with exact name |
| No cities configured | Check `CITY_1_PERSON` in `schedule.yml` |
| Weather fetch failed | Verify `QWEATHER_API_KEY` and `QWEATHER_API_HOST` |
| Gemini failed | Check `GEMINI_API_KEY` validity |
| Cron didn't trigger | 5–15 min delay is normal |

## Free Tier

- Public repos: **unlimited**
- Private repos: **2000 min/month**
- This script: ~1–2 min/run × 2/day = ~60 min/month ✅
