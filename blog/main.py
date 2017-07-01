from flask import render_template
from blog import app

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')