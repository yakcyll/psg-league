from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required

from app import app, db
from app.models import User, Match

from forms import AddMatchForm
from vendor import sgf


@app.route('/add_match', methods=['GET', 'POST'])
@login_required
def add_match():
    form = AddMatchForm()
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


