from openai import OpenAI
from dotenv import load_dotenv
import os
import json
import get_recipe

load_dotenv()

OpenAI.api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()

_cocktail_list = "스크류 드라이버, 보드카토닉, 모스크뮬, 마티니, 블랙 러시안, 롱 아일랜드 아이스티, 준벅, 미도리사워, 마가리타, 블루 라군"
_season = "가을"
_time = "저녁"
_weather = "눈"

def getDefaultRecommend(persona, cocktail_list, season, time, weather):
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
            "role": "system",
            "content": [
                {
                "text": "당신은 전문 칵테일 소믈리에입니다. 사용자에게 가장 적합한 칵테일을 추천하기 위해 사용자의 페르소나 정보를 바탕으로 추천을 제공합니다.\n당신은 20대 소믈리에이고 공손하지만 부담없는 말투를 갖고 있습니다.\n당신은 갖고 있는 칵테일 중 3종을 추천하고 그 이유를 50자 내로 설명합니다.\n칵테일은 \"name\" 태그, 추천 요소는 \"tag\"태그, 추천 이유는 \"reason\" 태그에 담아 json으로 제시합니다.\n당신은 [계절, 시간대, 날씨]를 입력 받고 각 요소에 대해 추천하는 칵테일 1종씩 총 3종을 추천합니다.\n추천은 항상 갖고 있는 칵테일에 포함된 칵테일만 작성합니다.\n추천하는 3종의 칵테일은 모두 다른 칵테일로 작성합니다.",
                "type": "text"
                }
            ]
            },
            {
            "role": "user",
            "content": [
                {
                "text": "제공된 페르소나는 다음과 같습니다: " + persona,
                "type": "text"
                }
            ]
            },
            {
            "role": "user",
            "content": [
                {
                "text": "당신이 갖고 있는 칵테일은 다음과 같습니다: " + cocktail_list,
                "type": "text"
                }
            ]
            },
            {
            "role": "user",
            "content": [
                {
                "text": "당신은 [" + season + ", " + time + ", " + weather + "]에 대해서 추천합니다.",
                "type": "text"
                }
            ]
            }
        ],
        response_format={
            "type": "json_object"
        },
        temperature=1,
        max_tokens=2048,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    print(response)
    print("end of response\n")
    j = response.choices[0].message.content
    formateed_json = json.dumps(j, ensure_ascii=False, indent=4)
    print(j)

    return formateed_json 