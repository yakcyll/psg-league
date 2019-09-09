from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user
from app import app
from app.models import User
from forms.login_form import LoginForm

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

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Niewłaściwa nazwa użytkownika bądź hasło')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))

    return render_template('login.html', title='Logowanie', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
