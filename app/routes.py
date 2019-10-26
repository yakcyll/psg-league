from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from datetime import datetime

from app import app, db
from app.models import User, Match
from forms import LoginForm, RegistrationForm, EditProfileForm, AddMatchForm

from vendor import sgf

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

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Gratulacje, rejestracja powiodła się!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

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

        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)

    return render_template('login.html', title='Logowanie', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/user/<id>')
@login_required
def user(id):
    if id.isdigit():
        user = User.query.filter_by(id=id).first_or_404()
    else:
        user = User.query.filter_by(username=id).first_or_404()

    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'},
    ]
    matches = Match.query.filter_by(black_player_id=user.id).union(Match.query.filter_by(white_player_id=user.id)).all()
    return render_template('user.html', user=user, posts=posts, matches=matches)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Twoje zmiany zostały zapisane.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edytuj profil', form=form)

@app.route('/add_match', methods=['GET', 'POST'])
@login_required
def add_match():
    form = AddMatchForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            black_player = User.query.filter_by(username=form.black_player.data).first()
            white_player = User.query.filter_by(username=form.white_player.data).first()
            if black_player is None:
                flash('W systemie nie zarejestrowano użytkownika o podanym imieniu czarnego gracza.')
                return redirect(url_for('add_match'))
            if white_player is None:
                flash('W systemie nie zarejestrowano użytkownika o podanym imieniu białego gracza.')
                return redirect(url_for('add_match'))

            sgf_data = None
            collection = sgf.Collection(sgf.Parser())
            try:
                sgf_data = request.files.get('sgf_file').read().decode('utf-8')
                collection.parser.parse(sgf_data)
            except (UnicodeDecodeError, sgf.ParseException):
                flash('Wgrany plik nie jest poprawnym plikiem SGF.')
                return redirect(url_for('add_match'))

            match = Match(black_player=black_player, white_player=white_player, sgf=sgf_data, result=collection[0].nodes[0].properties['RE'][0])
            db.session.add(match)
            db.session.commit()
            flash('Twój mecz został zapisany.')
            return redirect(url_for('add_match'))
    return render_template('add_match.html', title='Dodaj mecz', form=form)

@app.route('/match/<id>')
def view_match(id):
    match = Match.query.filter_by(id=id).first_or_404()
    title = 'Mecz ' + match.black_player.username + ' vs. ' + match.white_player.username

    return render_template('view_match.html', title=title, match=match)

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
