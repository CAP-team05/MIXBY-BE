from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()

OpenAI.api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()

with open('reco_codes/_userInfo.json') as f1:
    user_data = json.load(f1)

with open('reco_codes/_tastingNotes.json') as f2:
    tasting_data = json.load(f2)

def getDrinkList():
    drinkList = []
    r = ""
    for item in tasting_data:
        _str = "["
        _str += item["name"] + ", " + item["date"] + ", " + item["tag1"] + ", " + item["tag2"] + ", " + item["eval"] + ", " + item["sweetness"] + ", " + item["sourness"] + ", " + item["alcohol"]
        _str += "]"
        drinkList.append(_str)
    for i in drinkList:
        r += i + ", "
    return r

print(getDrinkList())

def getSummary():
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": [
                    {
                        "type": "text",
                        "text": "당신은 전문 칵테일 소믈리에입니다.\n사용자에게 가장 적합한 칵테일을 추천하기 위해 사용자의 페르소나 정보를 요약하는 역할을 맡고 있습니다.\n사용자의 정보는 [이름, 나이, 선호하는 맛]로 입력됩니다.\n사용자가 먹은 칵테일은 [칵테일 이름, 사용자가 먹은 날짜, 칵테일 특징1, 칵테일 특징2, 사용자의 해당 칵테일 선호도, 해당 칵테일 단맛 평가, 해당 칵테일 산미 평가, 해당 칵테일 도수 평가]로 입력됩니다.\n사용자에 대한 정보와 먹어봤던 칵테일에 대한 설명을 보고 100자 정도로 사용자를 요약합니다.\n요약에 대한 설명은 Json으로 반환하며 태그 이름은 \"summary\"입니다.\n칵테일에 대한 특징을 반영한 요약을 제시합니다."
                    }
                ]
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "사용자 정보는 다음과 같습니다: " + user_data[0]["name"] + ", " + user_data[0]["gender"] + ", " + user_data[0]["prefer"]
                    }
                ]
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "지금까지 사용자가 먹은 칵테일을 다음과 같습니다: " + getDrinkList()
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
    print(j)

    ret = json.loads(j)["summary"]

    return ret

cocktail_list = "스크류 드라이버, 보드카토닉, 모스크뮬, 마티니, 블랙 러시안, 롱 아일랜드 아이스티, 준벅, 미도리사워, 마가리타, 블루 라군"
season = "가을"
time = "저녁"
weather = "눈"

def getDefaultRecommend():
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
            "role": "system",
            "content": [
                {
                "text": "당신은 전문 칵테일 소믈리에입니다. 사용자에게 가장 적합한 칵테일을 추천하기 위해 사용자의 페르소나 정보를 바탕으로 추천을 제공합니다.\n당신은 20대 소믈리에이고 공손하지만 부담없는 말투를 갖고 있습니다.\n당신은 갖고 있는 칵테일 중 3종을 추천하고 그 이유를 설명합니다.\n칵테일은 \"name\" 태그, 추천 요소는 \"tag\"태그, 추천 이유는 \"reason\" 태그에 담아 json으로 제시합니다.\n당신은 [계절, 시간대, 날씨]를 입력 받고 각 요소에 대해 추천하는 칵테일 1종씩 총 3종을 추천합니다.\n추천은 항상 갖고 있는 칵테일에 포함된 칵테일만 작성합니다.\n추천하는 3종의 칵테일은 모두 다른 칵테일로 작성합니다.",
                "type": "text"
                }
            ]
            },
            {
            "role": "user",
            "content": [
                {
                "text": "제공된 페르소나는 다음과 같습니다: " + getSummary(),
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

    #ret = json.loads(j)["reason"]

    return formateed_json


print(getDefaultRecommend())
# print(getSummary())