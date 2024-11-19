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

# response = client.chat.completions.create(
#     model="gpt-3.5-turbo",
#     messages=[
#         { "role": "system", "content": "You are a helpful assistant designed to output JSON." },
#         { "role": "user", "content": "당신은 칵테일 3종을 추천하는 바텐더이다." },
#         { "role": "user", "content": "당신은 추천하는 이유를 1회 종합적으로 제시한다."},
#         { "role": "user", "content": "우리가 갖고 있는 칵테일은 다음과 같습니다: " + ", ".join(cocktails) },
#         { "role": "assistant", "content": "당신은 밤에 어울리는 칵테일을 추천합니다." }
#     ]
# )

"""
현재 추천 LLM 진행 중
to-do : 여러 요소를 한 번에 받고 한번에 리턴해주기 (ex. 계절, 날씨, 시간대)
"""
response = client.chat.completions.create(
  model="gpt-4o-mini",
  messages=[
    {
      "role": "system",
      "content": [
        {
          "text": "당신은 칵테일 바텐더이며 칵테일을 추천하는 역할을 맡고 있다.\n당신은 갖고 있는 칵테일 중 3종을 추천하고 그 이유를 함께 json으로 제시한다.\n모든 추천의 이유는 반드시 \"~요\"로 끝나야 한다. 예를 들어, 이런 상황이 특징이에요, 이런 상황에 잘 어울려요, 이런 식으로 끝나야 한다.",
          "type": "text"
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "text": "당신은 이유의 분량을 한 문장 정도로 제시한다.",
          "type": "text"
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "text": "당신이 갖고 있는 칵테일은 스크류 드라이버, 보드카토닉, 모스크뮬, 마티니, 블랙 러시안, 롱 아일랜드 아이스티이다.",
          "type": "text"
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "text": "당신은 가을에 어울리는 칵테일을 추천한다.",
          "type": "text"
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "text": "{\n  \"추천_칵테일\": [\n    {\n      \"이름\": \"모스크뮬\",\n      \"이유\": \"가을의 상큼한 맛과 향이 잘 어울려요.\"\n    },\n    {\n      \"이름\": \"롱 아일랜드 아이스티\",\n      \"이유\": \"모든 계절에 함께하기 좋지만, 가을에도 그 풍부한 맛이 즐거움을 더해요.\"\n    },\n    {\n      \"이름\": \"블랙 러시안\",\n      \"이유\": \"허브나 커피 맛이 가을의 따스함과 잘 어우러져요.\"\n    }\n  ]\n}",
          "type": "text"
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "겨울에 어울리는 칵테일 추천해줘."
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "type": "text",
          "text": "{\n  \"추천_칵테일\": [\n    {\n      \"이름\": \"마티니\",\n      \"이유\": \"겨울의 차분한 분위기와 잘 어울리는 클래식한 맛이 매력적이에요.\"\n    },\n    {\n      \"이름\": \"블랙 러시안\",\n      \"이유\": \"커피 리큐어가 포함되어 있어 따뜻한 느낌을 주며 겨울에 잘 어울려요.\"\n    },\n    {\n      \"이름\": \"모스크뮬\",\n      \"이유\": \"생강 맥주와 라임이 더해져 상큼하면서도 따뜻한 기분을 느낄 수 있어요.\"\n    }\n  ]\n}"
        }
      ]
    }
  ],
  temperature=1,
  max_tokens=2048,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0,
  response_format={
    "type": "json_object"
  }
)


result = response.choices[0].message
print(result)
# print(response)