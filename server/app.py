from flask import Flask, render_template, request, make_response
from backend import *
import os
import logging


app = Flask(__name__, template_folder='pages')
log = logging.getLogger('werkzeug')
log.disabled = True

codes = []
game = None


def read_key():
    """ read flask key from file """
    with open('./key.txt', 'r') as f:
        key = f.read()
    return key


'''@app.route('/', methods=['GET'])
def home():
    if request.method == 'GET':
        nickname = request.cookies.get('nickname')
        resp = make_response(render_template('home.html', nickname=nickname))
        return resp'''

 
@app.route('/', methods=['GET'])
def home():
    global game 

    # debug mode
    if game == None:
        game = start_game()
    else:
        start = request.args.get("move_start")
        desti = request.args.get("move_desti")
        game.play(start, desti)

    nickname = 'debug player 1'
    opponent = 'debug player 2'
    board = game.get_board_state()
    print(game.board)

    return render_template('game.html', nickname=nickname, board=board, opponent=opponent)

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
        global codes
        err_msg = ""
        nickname = request.cookies.get('nickname')
        code = request.form.get('code')

        try:
            code = int(code)
        except ValueError as e:
            err_msg = 'Code is not of type int.'
            return render_template('home.html', nickname=nickname, msg=err_msg)

        code_obj = get_code(codes, code)

        if code_obj:
            if code_obj.is_expired():
                err_msg = 'Code has expired.'
            # allow this for testing
            #if code_obj.owner == nickname:
            #   err_msg = 'Cannot join your own game.'
        else:
            err_msg = 'Code does not exist.'

        game = start_game() 
        board = game.get_board_state()

        if err_msg:
            resp = render_template('home.html', nickname=nickname, msg=err_msg)
        else:
            resp = render_template('game.html', nickname=nickname, board=board) # add opponent nick too

        return resp


@app.route('/generate-game-code', methods=['GET'])
def generate_game_code():
    if request.method == 'GET':
        global codes
        nickname = request.cookies.get('nickname')
        code = Code(owner=nickname)
        codes.append(code)

        resp = make_response(render_template('home.html', nickname=nickname, code=code.code))
        return resp


if __name__ == '__main__':
    app.secret_key = read_key()
    port = int(os.environ.get('PORT', 1337))
    app.run(host='0.0.0.0', port=port)