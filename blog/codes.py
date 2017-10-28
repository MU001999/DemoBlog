# -*- coding: utf-8 -*-

import os
from flask import render_template, redirect, request, session
from blog import app
from blog.link2db import *


@app.route('/codes/paste', methods=['GET', 'POST'])
def paste_code():
    if request.method == 'GET':
        return render_template('/codes/codePaste.html')

    poster, syntax, content = request.form['poster'], request.form['syntax'], request.form['content']
    return redirect('/codes/'+str(add_code(poster, syntax, content)))


@app.route('/codes/<int:code_id>')
def set_code(code_id):
    poster, syntax, content = get_code(code_id)
    return render_template('/codes/code.html', poster=poster, syntax=syntax, content=content)
