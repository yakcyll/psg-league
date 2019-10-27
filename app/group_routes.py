from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required

from app import app, db
from app.models import User, PlayingGroup

from forms import CreateGroupForm


@app.route('/create_group', methods=['GET', 'POST'])
@login_required
def create_group():
    form = CreateGroupForm()
    if form.validate_on_submit():
        group = PlayingGroup(name=form.name.data, notes=form.notes.data, hidden=form.hidden.data)
        db.session.add(group)
        db.session.commit()

    return render_template('create_group.html', title="Utwórz grupę ligową", form=form)
