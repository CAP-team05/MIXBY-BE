from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

# response = openai.chat.completions.create(
#     model="gpt-3.5-turbo",
#     response_format={ "type": "json" },
#     messages=[
#         { "role": "system", "content": "You are a helpful assistant designed to output JSON" },
#         { "role": "user", "content": "당신은 칵테일 3종을 추천하는 바텐더이며 해당 칵테일을 추천하는 이유를 함께 제시한다" },
#         { "role": "assistant", "content": "당신은 겨울에 어울리는 칵테일을 추천합니다." }
#     ]
# )

# response = openai.Completion.create(
#     engine="gpt-3.5-turbo",
#     prompt="당신은 칵테일 3종을 추천하는 바텐더이며 해당 칵테일을 추천하는 이유를 함께 제시한다",
#     max_tokens=100
# )

OpenAI.api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()
# response = client.chat.completions.create(
#     model="gpt-3.5-turbo",
#     messages=[
#         { "role": "system", "content": "You are a helpful assistant designed to output JSON" },
#         { "role": "user", "content": "당신은 칵테일 3종을 추천하는 바텐더이며 해당 칵테일을 추천하는 이유를 함께 제시한다" },
#         { "role": "assistant", "content": "당신은 겨울에 어울리는 칵테일을 추천합니다." }
#     ]
# )

cocktails = [
    "스크류 드라이버",
    "보드카토닉",
    "모스크뮬",
    "마티니",
    "블랙 러시안",
    "롱 아일랜드 아이스티"
]

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        { "role": "system", "content": "You are a helpful assistant designed to output JSON." },
        { "role": "user", "content": "당신은 칵테일 3종을 추천하는 바텐더이다." },
        { "role": "user", "content": "당신은 추천하는 이유를 1회 종합적으로 제시한다."},
        { "role": "user", "content": "우리가 갖고 있는 칵테일은 다음과 같습니다: " + ", ".join(cocktails) },
        { "role": "assistant", "content": "당신은 밤에 어울리는 칵테일을 추천합니다." }
    ]
)

result = response.choices[0].message
print(result)
# print(response)