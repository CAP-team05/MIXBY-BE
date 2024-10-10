from flask import Flask, jsonify, render_template

import json
import getinfo

app = Flask(__name__)

@app.route('/')  # '/' 경로 접속 시 start 실행 (라우팅 이라고 부름)
def start():  # 함수의 이름은 중복만 되지 않으면 됨
    return "믹스비 어플 개발중..."

# show all drink
@app.route('/drink')
def drinks():
    return app.response_class(
        response=json.dumps(getinfo.getalldrinks(), indent=4),
        mimetype='application/json'
    )
# search drinks including <code> at name or code
@app.route('/drink/<code>')
def drink(code):
    info = getinfo.getdrink(code)
    return app.response_class(
        response=json.dumps(info, indent=4),
        mimetype='application/json'
    )

# show all recipe
@app.route('/recipe')
def recipes():
    return app.response_class(
        response=json.dumps(getinfo.getallrecipes(), indent=4),
        mimetype='application/json'
    )
# search recipes including <code> at name or code
@app.route('/recipe/<code>')
def recipe(code):
    info = getinfo.getrecipe(code)
    return app.response_class(
        response=json.dumps(info, indent=4),
        mimetype='application/json'
    )

@app.route('/yee')
def yee():
    return render_template('myimage.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2222)  # app 실행