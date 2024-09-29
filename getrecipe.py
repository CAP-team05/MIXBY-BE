import requests
import json
import string

# 저장할 리스트 초기화
all_cocktails = []

# 모든 알파벳을 순차적으로 호출
for letter in string.ascii_lowercase:
    url = f"https://www.thecocktaildb.com/api/json/v1/1/search.php?f={letter}"
    response = requests.get(url)
    data = response.json()

    # 'drinks'가 None이 아닐 때만 데이터 병합
    if data['drinks'] is not None:
        all_cocktails.extend(data['drinks'])

# 모든 데이터를 하나의 JSON 파일로 저장
with open('data_recipe_cocktaildb.json', 'w') as f:
    json.dump(all_cocktails, f, indent=4)

print(f"{len(all_cocktails)}개의 칵테일 데이터가 저장되었습니다.")
