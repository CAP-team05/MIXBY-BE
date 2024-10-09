import requests, json, string

all_cocktails = []

for letter in string.ascii_lowercase:
    url = f"https://www.thecocktaildb.com/api/json/v1/1/search.php?f={letter}"
    response = requests.get(url)
    data = response.json()

    if data['drinks'] is not None:
        all_cocktails.extend(data['drinks'])

with open('data_recipe_cocktaildb.json', 'w') as f:
    json.dump(all_cocktails, f, indent=4)

print(f"{len(all_cocktails)}개의 칵테일 데이터가 저장되었습니다.")
