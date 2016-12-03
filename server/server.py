#!/usr/bin/env python3

from flask import Flask, render_template, g
import base64
import hashlib
import os
import shelve


app = Flask(__name__)

# little hack to this working on Flask development server
scores_dict = None
scores_dict = scores_dict or shelve.open('scores')


# Add flags here mapping to their number in our list. For sure a better way
# to go about this, but this is quick and dirty. Also should we standardize
# flag format lol?
flag_map = {
    'flag{gary-ignatius-teabody}': 12,
    'pan galactic gargle blaster': 21,
    'FLAG{c_is_the_best_and_you_should_all_learn_it}': 15,
    'flag{:poopemoji:}': 14,
}


def get_salted_hash(username, actual_flag):
    sha = hashlib.sha1()
    sha.update(bytes(username + ':' + actual_flag, 'ascii'))
    return base64.b16encode(sha.digest())


@app.route('/submit/<string:username>')
@app.route('/submit/<string:username>/')
@app.route('/submit/<string:username>/<string:flag>')
def handle_flag_submit(username, flag=None):
    completed = scores_dict[username] if username in scores_dict else set()

    response = 'hi {}<br><br>'.format(username)

    if flag:
        flag = bytes(flag.upper(), 'ascii')
        for actual_flag in flag_map:
            if flag == get_salted_hash(username, actual_flag):
                completed.add(flag_map[actual_flag])
                scores_dict[username] = completed

                print('{} completed {}'.format(username, flag_map[actual_flag]))

    if len(completed) > 0:
        response += 'completed: {}'.format(', '.join(map(str, completed)))
    else:
        response += 'you haven\'t found anything yet :('

    return response


def make_hint_links():
    pages = filter(lambda x: len(x.split('.')) == 2, os.listdir('hints'))
    pages = [(int(x.split('.')[0]), 'hints/' + x) for x in pages]
    pages.sort(key=lambda x: x[1])
    pages = ['<a href="' + x[1] + '">' + str(x[0]) + '</a>' for x in pages]

    return '<br><br><br><strong>Hints</strong><br>' + ' '.join(pages)


def serve_hint(page):
    with open('hints/' + page) as f:
        return f.read()


def make_leaderboards():
    board = list(map(lambda x: (x[0], len(x[1])), scores_dict.items()))
    board.sort(key=lambda x: -x[1])

    i = 1
    last_place = 0
    last_score = 100

    leaderboards = '<br><br><br><strong>Leaderboards</strong><br>'

    if len(board) == 0:
        return leaderboards + 'Nobody!'

    for user in board:
        if user[1] != last_score:
            last_place = i
        leaderboards += '{}. {}<br>'.format(last_place, user[0])
        i += 1
        last_score = user[1]

    return leaderboards


@app.route('/')
def index():
    hints = sorted(flag_map.values())
    board = sorted((n, len(fs)) for n, fs in scores_dict.items())
    return render_template('index.html', hints=hints, board=board)


@app.route('/hints/<int:hint>')
def hints(hint):
    return render_template('%d.html' % hint)


@app.errorhandler(404)
@app.errorhandler(500)
def error(err):
    return 'not a page :('


if __name__ == '__main__':
    app.run(threaded=False)
