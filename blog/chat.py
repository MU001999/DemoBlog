# -*- coding: utf-8 -*-

import time
from flask import render_template, redirect, request, session, jsonify
from flask_socketio import join_room, leave_room, send, emit
from blog import socketio, app
from blog.link2db import *


nicks = set()


@app.route('/chat')
def set_chat():
    return render_template('/chat/chat.html')


@app.route('/chat/check', methods=['POST'])
def check():
    global nicks
    if request.form['nick'] in nicks:
        return "exist"
    else:
        return "noexist"


@socketio.on('join')
def on_join(data):
    nickname = data['nickname']
    room = data['room']
    join_room(room)

    global nicks
    nicks.add(nickname)
    emit('change_num', str(len(nicks)), room=room)

    send(u'【' + nickname + u'】' + u' 已经准备好瞎侃了，', room=room)


@socketio.on('send_msg')
def on_send_msg(data):
    nickname = data['nickname']
    room = data['room']
    msg = data['msg']
    emit('recv_msg', {'nickname': nickname, 'msg': msg, 'time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}, room=room)


@socketio.on('leave')
def on_leave(data):
    nickname = data['nickname']
    room = data['room']
    leave_room(room)

    global nicks
    nicks.remove(nickname)
    emit('change_num', str(len(nicks)), room=room)

    send(u'【' + nickname + u'】' + u' 认真学习去了，', room=room)
