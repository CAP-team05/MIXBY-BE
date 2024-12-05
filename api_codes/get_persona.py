from openai import OpenAI
from dotenv import load_dotenv
import os
import json
import get_recipe

load_dotenv()

OpenAI.api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()


def getDrinkList(tasting_data):
    drinkList = []
    r = ""
    for item in tasting_data:
        _d = get_recipe.search_bycode(item["code"])
        _str = "["
        _str += _d["korean_name"] + ", " + item["drinkDate"] + ", " + _d["tag1"] + ", " + _d["tag2"] + ", " + to_eval(item["eval"]) + ", " + to_eval(item["sweetness"]) + ", " + to_eval(item["sourness"]) + ", " + to_eval(item["alcohol"])
        _str += "]"
        drinkList.append(_str)
    for i in drinkList:
        r += i + ", "
    return r

def to_eval(n: int) -> str:
    eval_mapping = {
        0: "매우 불만",
        1: "대체로 불만",
        2: "조금 불만",
        3: "보통",
        4: "조금 만족",
        5: "대체로 만족",
        6: "매우 만족"
    }
    return eval_mapping.get(n, str(n))

# print(getDrinkList())

def getPersona(user_data, tasting_data):
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
                        "text": "사용자 정보는 다음과 같습니다: " + user_data[0]["name"] + ", " + user_data[0]["gender"] + ", " + user_data[0]["favoriteTaste"]
                    }
                ]
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "지금까지 사용자가 먹은 칵테일을 다음과 같습니다: " + getDrinkList(tasting_data)
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