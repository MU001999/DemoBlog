# -*- coding: utf-8 -*-

import os
from flask import render_template, redirect, request, session
from blog import app
from blog.link2db import *


@app.route('/article', methods=['GET', 'POST'])
def paste_code():
    if not session['logged_in']:
        return redirect('/')
    if request.method == 'GET':
        return render_template('article.html')
    return render_template('article.html')
