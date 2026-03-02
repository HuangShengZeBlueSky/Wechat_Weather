import requests

def test_qweather_custom_host():
    print("\n=== 测试和风天气 (专属 API Host) ===")
    key = "6c9427bb021045838d59fa6e8b605fc7"  # 记得换成你新生成的 Key
    
    # 重点在这里：把 devapi.qweather.com 换成你的专属 apihost
    url = "https://pc5ctvmrbk.re.qweatherapi.com/v7/weather/now" 
    
    headers = {"X-QW-Api-Key": key}
    params = {"location": "101010100"} # 101010100 是北京的城市代码，你可以换成目标城市
    
    try:
        r = requests.get(url, headers=headers, params=params, timeout=10)
        print(f"  Status: {r.status_code}")
        
        # 将返回的 JSON 字符串解析为字典并美化打印
        import json
        print(f"  Response:\n{json.dumps(r.json(), indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"  ERROR: {e}")

test_qweather_custom_host()