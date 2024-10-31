from flask import Flask, jsonify, render_template

import get

app = Flask(__name__)

@app.route('/')  # '/' 경로 접속 시 start 실행 (라우팅 이라고 부름)
def start():  # 함수의 이름은 중복만 되지 않으면 됨
    return "믹스비 어플 개발중..."

@app.route('/product/<code>')
def barcode(code):
    if code == "all": return get.getall()
    info = get.getinfo(code)
    return info

@app.route('/recipe/<code>')
def recipe(code):
    if code == "all": return "구현 예정!"
    info = "구현 예정!"
    return info

@app.route('/yee')
def yee():
    return render_template('myimage.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2222)  # app 실행
