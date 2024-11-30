import requests
import os
from dotenv import load_dotenv

# .env 파일에서 API 키 로드
load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")

def get_weather_by_location(latitude, longitude):
    """
    OpenWeather API를 사용하여 주어진 위도와 경도의 날씨 데이터를 받아 JSON으로 반환하는 함수

    Args:
        latitude (float): 위도
        longitude (float): 경도

    Returns:
        dict: 날씨 정보가 담긴 JSON 데이터
    """
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "lat": latitude,
        "lon": longitude,
        "appid": API_KEY,
        "units": "metric",  # 섭씨 온도
        "lang": "kr"       # 한국어 응답
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # 상태 코드가 200이 아니면 예외 발생
        print(response.json())
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
        return {"error": str(e)}