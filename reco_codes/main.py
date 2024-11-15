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
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        { "role": "system", "content": "You are a helpful assistant designed to output JSON" },
        { "role": "user", "content": "당신은 칵테일 3종을 추천하는 바텐더이며 해당 칵테일을 추천하는 이유를 함께 제시한다" },
        { "role": "assistant", "content": "당신은 겨울에 어울리는 칵테일을 추천합니다." }
    ]
)


result = response.choices[0].message
print(result)
print(response)