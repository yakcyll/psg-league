from flask import render_template, flash, redirect, url_for
from app import app
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
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Logowanie', form=form)
