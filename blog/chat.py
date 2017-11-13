# -*- coding: utf-8 -*-

import time
from flask import render_template, redirect, request, session
from flask_socketio import join_room, leave_room, send, emit
from blog import socketio, app
from blog.link2db import *


@app.route('/chat')
def set_chat():
    return render_template('/chat/chat.html')


@socketio.on('join')
def on_join(data):
    nickname = data['nickname']
    room = data['room']
    join_room(room)
    send(nickname + ' has entered the room.', room=room)


@socketio.on('send_msg')
def on_send_msg(data):
    nickname = data['nickname']
    room = data['room']
    msg = data['msg']
    emit('recv_msg', {'nickname': nickname, 'msg': msg}, room=room)


@socketio.on('leave')
def on_leave(data):
    nickname = data['nickname']
    room = data['room']
    leave_room(room)
    send(nickname + 'has left the room.', room=room)
