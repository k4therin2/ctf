#!/usr/bin/env python3

from flask import Flask
import base64
import hashlib
import os
import shelve


scores_dict = None


# Add flags here mapping to their number in our list. For sure a better way
# to go about this, but this is quick and dirty. Also should we standardize
# flag format lol?
flag_map = {
    'flag{gary-ignatius-teabody}': 12,
    'pan galactic gargle blaster': 21,
    'FLAG{c_is_the_best_and_you_should_all_learn_it}': 15,
    'flag{:poopemoji:}': 14,
    'flaggetmeout': 39,
}


def get_salted_hash(username, actual_flag):
    sha = hashlib.sha1()
    sha.update(bytes(username + ':' + actual_flag, 'ascii'))
    return base64.b16encode(sha.digest())


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


if __name__ == '__main__':
    scores_dict = shelve.open('scores')

    with open('index.html') as f:
        index = f.read()

    app = Flask('ctf_leaderboards')

    app.route('/')(lambda: index + make_hint_links() + make_leaderboards())

    app.route('/hints/<string:page>')(serve_hint)

    app.route('/submit/<string:username>')(handle_flag_submit)
    app.route('/submit/<string:username>/')(handle_flag_submit)
    app.route('/submit/<string:username>/<string:flag>')(handle_flag_submit)

    app.errorhandler(404)(lambda x: 'not a page :(')
    app.errorhandler(500)(lambda x: 'not a page :(')

    app.run(host='0.0.0.0')
