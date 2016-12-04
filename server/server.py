#!/usr/bin/env python3

import base64
import hashlib
import os
import os.path

from flask import Flask, render_template, g
from flask_cas import CAS, login_required
from flask_shelve import get_shelve, init_app

from emailhint import send_hint
from linkedlist import LINKED_LIST, LL_END


app = Flask(__name__)
app.config['CAS_SERVER'] = 'https://login.case.edu'
app.config['CAS_AFTER_LOGIN'] = 'index'
app.config['SHELVE_FILENAME'] = 'scores'
cas = CAS(app, '/cas')
init_app(app)
EMAIL_ENABLED = False


# Add flags here mapping to their number in our list. For sure a better way
# to go about this, but this is quick and dirty. Also should we standardize
# flag format lol?
flag_map = {
    'flag{I_lied_this_is_a_flag}': 1,
    'flag{spoofer_no_spoofing}': 2,
    'flag{All men are created equal}': 3,
    'flag{touch_and_go}': 4,
    'flag{never_break_the_chain}': 6,
    'flag{gary-ignatius-teabody}': 12,
    'flag{mailto:has_somebody_pooped@case.edu}': 13,
    'flag{:poopemoji:}': 14,
    'FLAG{c_is_the_best_and_you_should_all_learn_it}': 15,
    'flag{joe_biden}': 19,
    'flag{Leeroy Jenkins}': 20,
    'flag{pan galactic gargle blaster}': 21,
    'Flag{My_Homo_is_erectus}': 22,
    'flaggetmeout': 39,
    'flag{R2_deet_doot}': 18,
    'flag{dat_tswizzle_reference_tho}': -1,
    'flag{camelCaseFlagForTheWin}': 23,
}


def get_salted_hash(username, actual_flag):
    sha = hashlib.sha1()
    sha.update(bytes(username + ':' + actual_flag, 'ascii'))
    return base64.b16encode(sha.digest())


@app.route('/score/<string:username>')
def score(username):
    scores_dict = get_shelve('r')
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
    scores_dict = get_shelve('w')
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
        completed=map(str, completed) if completed else None,
        just_completed=just_completed,
        username=username,
        flag=flag
    )


@app.route('/')
def index():
    scores_dict = get_shelve('r')
    hints = [x for x in sorted(flag_map.values()) if x > 0]
    board = sorted(((n, ', '.join(map(str, fs))) for n, fs in scores_dict.items()),
                   key=lambda x: len(x[1].split(',')), reverse=True)
    return render_template('index.html', hints=hints, board=board,
                           username=cas.username)


@app.route('/hints/<int:hint>')
def hints(hint):
    if hint <= 0:
        return 'this is probably not a flag', 404
    scores_dict = get_shelve('r')
    solvedit = [u for u, l in scores_dict.items() if hint in l]
    return render_template('%d.html' % hint, username=cas.username,
                           solvedit=solvedit)


@app.route('/linkedlist/<int:addr>')
def linkedlist(addr):
    if addr == LL_END:
        return 'flag{never_break_the_chain}'
    if addr not in LINKED_LIST:
        return "That's not part of the list!", 404
    next_addrs = LINKED_LIST[addr]
    if len(next_addrs) == 2: # fork
        return 'next: %d\nbut the real one is: %d' % tuple(next_addrs)
    else:
        return 'next: %d' % next_addrs[0]


@app.route('/emailme')
@login_required
def emailme():
    # I'm sure this could be flaky, so I'm providing a mechanism to disable it,
    # and the email script is outside so that an organizer can manually send
    # the email.
    if not EMAIL_ENABLED:
        return render_template('email.html', success=False)
    try:
        send_hint(cas.username + '@case.edu')
    except:
        print('ERROR SENDING EMAIL')
        return render_template('email.html', success=False)
    return render_template('email.html', success=True, msg='Check your email!')


@app.errorhandler(404)
@app.errorhandler(500)
def error(err):
    return 'not a page :('


if not os.path.exists('secret'):
    print('NOTE: New secret key. All sessions lost.')
    with open('secret', 'wb') as f:
        f.write(os.urandom(24))
with open('secret', 'rb') as f:
    app.secret_key = f.read(24)


if __name__ == '__main__':
    app.run()
