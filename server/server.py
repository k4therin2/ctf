#!/usr/bin/env python3

import base64
import hashlib
import os
import os.path
import shelve

from flask import Flask, render_template, g
from flask.ext.cas import CAS, login_required


app = Flask(__name__)
cas = CAS(app, '/cas')
app.config['CAS_SERVER'] = 'https://login.case.edu'
app.config['CAS_AFTER_LOGIN'] = 'index'
app.config['CAS_AFTER_LOGOUT'] = 'index'

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


@app.route('/score/<string:username>')
def score(username):
    completed = scores_dict[username] if username in scores_dict else set()
    return render_template(
        "score.html",
        completed=map(str, completed),
        score_for=username,
        username=cas.username,
    )

@app.route('/submit/<string:flag>')
@login_required
def handle_flag_submit(flag=None):
    username = cas.username
    completed = scores_dict[username] if username in scores_dict else set()
    just_completed = None

    flag = bytes(flag.upper(), 'ascii')
    for actual_flag in flag_map:
        if flag == get_salted_hash(username, actual_flag):
            just_completed = flag_map[actual_flag]
            completed.add(just_completed)
            scores_dict[username] = completed
            print('{} completed {}'.format(username, flag_map[actual_flag]))

    return render_template(
        "completed.html",
        completed=map(str, completed),
        just_completed=just_completed,
        username=username,
        flag=flag
    )


@app.route('/')
def index():
    hints = sorted(flag_map.values(), reverse=True)
    board = sorted((n, len(fs)) for n, fs in scores_dict.items())
    return render_template('index.html', hints=hints, board=board,
                           username=cas.username)


@app.route('/hints/<int:hint>')
def hints(hint):
    return render_template('%d.html' % hint, username=cas.username)


@app.errorhandler(404)
@app.errorhandler(500)
def error(err):
    return 'not a page :('


if __name__ == '__main__':
    if not os.path.exists('secret'):
        print('NOTE: New secret key. All sessions lost.')
        with open('secret', 'wb') as f:
            f.write(os.urandom(24))
    with open('secret', 'rb') as f:
        app.secret_key = f.read(24)
    app.run(threaded=False)
