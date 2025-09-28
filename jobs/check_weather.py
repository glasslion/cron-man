import os
import sys
from pathlib import Path

import requests

sys.path.append(str(Path(__file__).parent.parent.resolve()))

from utils.wecomchan import send_wecomchan


def get_weather():
    # 使用的是 和风天气 API
    # Location ID 可查阅 https://github.com/qwd/LocationList
    location = 101021700  # 上海杨浦
    api_key = os.environ["QWEATHER_API_KEY"]
    url = f"https://nr7fbrqtr5.re.qweatherapi.com/v7/weather/now?key={api_key}&location={location}"
    r = requests.get(url)
    return r.json()


if __name__ == "__main__":
    weather = get_weather()
    if "雨" in weather["now"]["text"]:
        send_wecomchan("今天有雨，记得早点打车")
        print("已发送通知")
    else:
        print("无需发送通知")
