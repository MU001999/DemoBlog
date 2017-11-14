# -*- coding: utf-8 -*-

import os
from random import shuffle
from flask import render_template, redirect, request, session, abort
from flask_socketio import join_room, leave_room, send, emit
from blog import app


def compiler(language, code):
    if language == 'py':
        return 'py'
    elif language == 'cpp':
        return 'cpp'


@app.route('/play', methods=['GET', 'POST'])
def route_play():
    if request.method == 'GET':
        return render_template('/play/play.html')
    code = request.form['code']
    language = request.form['language']
    res = compiler(language, code)
    return render_template('/play/play.html', res=res)
