from flask import Flask, send_from_directory, jsonify, request, Response
from functools import wraps

import json
import get_drink, get_recipe, get_ingredients, get_persona, get_weather, get_recommend

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False  # 한글이 깨지지 않도록 설정

@app.route('/')  # '/' 경로 접속 시 start 실행 (라우팅 이라고 부름)
def start():  # 함수의 이름은 중복만 되지 않으면 됨
    return send_from_directory('static', 'api_rules.png')

# show all drink
@app.route('/drink/all')
def drinks():
    return app.response_class(
        response=json.dumps(get_drink.getalldrinks(), indent=4),
        mimetype='application/json'
    )
# show drink image
@app.route('/drink/image=<code>')
def drink_image(code=None):
    return send_from_directory('static', 'drinks/{}.png'.format(code))

# search drinks by <code>
@app.route('/drink/code=<code>')
def drink_code(code):
    info = get_drink.search_bycode(code)
    return app.response_class(
        response=json.dumps(info, indent=4),
        mimetype='application/json'
    )

# search drinks by <name>
@app.route('/drink/name=<name>')
def drink_name(name):
    info = get_drink.search_byname(name)
    return app.response_class(
        response=json.dumps(info, indent=4),
        mimetype='application/json'
    )

# search drinks by <type>
@app.route('/drink/type=<type>')
def drink_type(type):
    info = get_drink.search_bytype(type)
    return app.response_class(
        response=json.dumps(info, indent=4),
        mimetype='application/json'
    )


# show all recipe
@app.route('/recipe/all')
def all_recipes():
    return app.response_class(
        response=json.dumps(get_recipe.getallrecipes(), indent=4),
        mimetype='application/json'
    )
# show recipe image
@app.route('/recipe/image=<code>')
def recipe_image(code=None):
    return send_from_directory('static', 'recipes/{}.png'.format(code))

# search recipes by <name>
@app.route('/recipe/name=<name>')
def recipe_name(name):
    info = get_recipe.search_byname(name)
    return app.response_class(
        response=json.dumps(info, indent=4),
        mimetype='application/json'
    )

# search recipes by <code>
@app.route('/recipe/code=<code>')
def recipe_code(code):
    print(code)
    info = get_recipe.search_bycode(code)
    return app.response_class(
        response=json.dumps(info, indent=4),
        mimetype='application/json'
    )

# search available recipes
@app.route('/recipe/with=<codes>')
def recipe_with(codes):
    info = get_recipe.search_byings(codes)
    return app.response_class(
        response=json.dumps(info, indent=4),
        mimetype='application/json'
    )


# search ingredients by code
@app.route('/ing/with=<codes>')
def ing_code(codes):
    info = get_ingredients.getCode(codes)
    return app.response_class(
        response=json.dumps(info, indent=4),
        mimetype='application/json'
    )

# show ingredient image
@app.route('/ing/image=<name>')
def ing_image(name=None):
    return send_from_directory('static', 'ingredients/{}.png'.format(name))


def as_json(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        res = f(*args, **kwargs)
        res = json.dumps(res, ensure_ascii=False).encode('utf8')
        return Response(res, content_type='application/json; charset=utf-8')
    return decorated_function

# get persona / input : userInfo, tastingNote
@app.route('/persona', methods=['POST'])
@as_json
def userinfo():
    data = request.get_json()
    name = ""
    print(data)
    for item in data:
        if (item['ver'] == 'userInfo'):
            userData = item['content']
            name = item['content'][0]['name']
        elif (item['ver'] == 'tastingNote'):
            drinkData = item['content']

    persona = get_persona.getPersona(userData, drinkData)
    ret = {"name": name, "persona": persona}

    return ret

@app.route('/recommend', methods=['POST'])
@as_json
def recommmend():
    data = request.get_json()
    print(data)
    persona = data['persona']
    cocktail_list = data['cocktail_list']
    season = data['season']
    time = data['time']
    weather = data['weather']
    
    ret = get_recommend.getDefaultRecommend(persona, cocktail_list, season, time, weather)
    
    return ret

@app.route('/weather', methods=['POST'])
@as_json
def weather():
    data = request.get_json()
    latitude = data['latitude']
    longitude = data['longitude']
    
    ret = get_weather.get_weather_by_location(latitude, longitude)
    
    return {'weather_id': ret['weather'][0]['id'], 'weather_desc': ret['weather'][0]['description']}
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2222, debug=True)  # app 실행