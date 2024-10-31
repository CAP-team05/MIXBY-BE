from flask import Flask, jsonify, render_template

import json
import get_drink, get_recipe

app = Flask(__name__)

@app.route('/')  # '/' 경로 접속 시 start 실행 (라우팅 이라고 부름)
def start():  # 함수의 이름은 중복만 되지 않으면 됨
    return render_template('main.html')

# show all drink
@app.route('/drink/all')
def drinks():
    return app.response_class(
        response=json.dumps(get_drink.getalldrinks(), indent=4),
        mimetype='application/json'
    )
# search drinks including <code> at name or code
@app.route('/drink/<code>')
def drink(code):
    info = get_drink.getdrink(code)
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
@app.route('/recipe/image/<code>')
def recipe_image(code=None):
    return render_template('image_recipe.html', code=code)

# search recipes by name
@app.route('/recipe/name/<name>')
def recipe_name(name):
    info = get_recipe.getrecipe_byname(name)
    return app.response_class(
        response=json.dumps(info, indent=4),
        mimetype='application/json'
    )
# search recipes by code
@app.route('/recipe/code/<code>')
def recipe_code(code):
    info = get_recipe.getrecipe_bycode(code)
    return app.response_class(
        response=json.dumps(info, indent=4),
        mimetype='application/json'
    )
# search recipes by ingredients
@app.route('/recipe/ing/<ing>')
def recipe_ing(ing):
    info = get_recipe.getrecipe_byings(ing)
    return app.response_class(
        response=json.dumps(info, indent=4),
        mimetype='application/json'
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2222)  # app 실행