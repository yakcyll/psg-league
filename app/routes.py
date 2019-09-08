from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'world'}
    return render_template('index.html', title='Landing', user=user)

@app.route('/news')
def news():
    posts = [
        {
            'author': {'username': 'who'},
            'body': 'what',
        },
        {
            'author': {'username': 'where'},
            'body': 'when',
        },
    ]

    return render_template('news.html', title='News', posts=posts)
