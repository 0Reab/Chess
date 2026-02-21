from flask import Flask, render_template, request, make_response
from backend import *
import os


app = Flask(__name__, template_folder='pages')

codes = []


def read_key():
    """ read flask key from file """
    with open('./key.txt', 'r') as f:
        key = f.read()
    return key


@app.route('/', methods=['GET'])
def home():
    if request.method == 'GET':
        nickname = request.cookies.get('nickname')
        resp = make_response(render_template('home.html', nickname=nickname))
        return resp


@app.route('/set-nickname', methods=['POST'])
def set_nickname():
    if request.method == 'POST':
        nickname = request.form.get('nickname')

        resp = make_response(render_template('home.html', nickname=nickname))
        resp.set_cookie('nickname', nickname)

        return resp


@app.route('/join-game', methods=['POST'])
def join_game():
    if request.method == 'POST':
        code = request.form.get('code')
        nickname = request.cookies.get('nickname')
        msg = 'something went wong :p'

        code_obj = get_code(codes)

        if code_obj.is_expired():
            resp = render_template('home.html', nickname=nickname, msg=msg)
        else:
            resp = render_template('game.html', nickname=nickname) # add opponent nick too

        return resp


@app.route('/generate-game-code', methods=['GET'])
def generate_game_code():
    if request.method == 'GET':
        nickname = request.cookies.get('nickname')
        code = Code(owner=nickname)
        codes.append(code)

        resp = make_response(render_template('home.html', nickname=nickname, code=code.code))
        return resp


if __name__ == '__main__':
    app.secret_key = read_key()
    port = int(os.environ.get('PORT', 1337))
    app.run(host='0.0.0.0', port=port)