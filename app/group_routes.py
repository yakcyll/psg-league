from functools import wraps

from flask import render_template, flash, redirect, url_for, request, g
from flask_login import current_user, login_required

from app import app, db
from app.models import User, PlayingGroup

from forms import CreateGroupForm, EditGroupForm, ManageGroupsForm


def has_to_be_league_manager(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin and not current_user.is_league_manager:
            flash("Musisz być administratorem bądź zarządcą ligi, by móc otworzyć tę stronę.")
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/create_group', methods=['GET', 'POST'])
@login_required
@has_to_be_league_manager
def create_group():
    form = CreateGroupForm()
    if form.validate_on_submit():
        if PlayingGroup.query.filter_by(name=form.name.data).first() is not None:
            flash("Grupa o takiej nazwie już istnieje.")
            return redirect(url_for('create_group'))

        max_level = db.session.query(db.func.max(PlayingGroup.level)).scalar()
        max_level = 0 if max_level is None else max_level
        group = PlayingGroup(name=form.name.data, notes=form.notes.data, level=max_level+1, is_hidden=form.is_hidden.data)
        db.session.add(group)
        db.session.commit()
        return redirect(url_for('manage_groups'))

    return render_template('create_group.html', title="Utwórz grupę ligową", form=form)


@app.route('/edit_group/<groupid>', methods=['GET', 'POST'])
@login_required
@has_to_be_league_manager
def edit_group(groupid):
    group = PlayingGroup.query.filter_by(id=groupid).first()
    if group is None:
        flash("Grupa o danym identyfikatorze nie istnieje.")
        return redirect(url_for('manage_groups'))

    form = EditGroupForm()
    if form.validate_on_submit():
        group.name = form.name.data
        group.notes = form.notes.data
        group.is_hidden = form.is_hidden.data
        db.session.commit()
        flash("Modyfikacja grupy powiodła się.")
        return redirect(url_for('manage_groups'))
    elif request.method == 'GET':
        form.id.data = group.id
        form.name.data = group.name
        form.notes.data = group.notes
        form.is_hidden.data = group.is_hidden

    return render_template('edit_group.html', title="Edytuj grupę ligową", group=group, form=form)


@app.route('/manage_groups', methods=['GET', 'POST'])
@login_required
@has_to_be_league_manager
def manage_groups():
    form = ManageGroupsForm()

    groups = PlayingGroup.query.order_by('level').all()
    form.groups.choices = [(g.id, g.name if not g.is_hidden else g.name + " (H)") for g in groups]

    if not form.validate_on_submit() and request.method == 'POST':
        flash('Wybierz jedną z grup.')
        return redirect(url_for('manage_groups'))

    else:
        if form.move_up.data:
            group = PlayingGroup.query.filter_by(id=form.groups.data).first()
            group_up = PlayingGroup.query.filter_by(level=(group.level-1)).first()
            assert group is not None
            if group_up is not None:
                group.level -= 1
                group_up.level += 1
                db.session.commit()

        elif form.move_down.data:
            group = PlayingGroup.query.filter_by(id=form.groups.data).first()
            group_down = PlayingGroup.query.filter_by(level=(group.level+1)).first()
            assert group is not None
            if group_down is not None:
                group.level += 1
                group_down.level -= 1
                db.session.commit()

        elif form.edit.data:
            group = PlayingGroup.query.filter_by(id=form.groups.data).first()
            assert group is not None
            return redirect(url_for('edit_group', groupid=group.id))

    groups = PlayingGroup.query.order_by('level').all()
    form.groups.choices = [(g.id, g.name if not g.is_hidden else g.name + " (H)") for g in groups]

    return render_template('manage_groups.html', title="Zarządzaj grupami ligowymi", form=form)
