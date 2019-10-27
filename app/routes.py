from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required

from datetime import datetime

from app import app, db, user_routes, match_routes, group_routes


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'world'}
    if current_user.is_authenticated:
        user = current_user
    return render_template('index.html', title='Landing', user=user)

@app.route('/news')
@login_required
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

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
