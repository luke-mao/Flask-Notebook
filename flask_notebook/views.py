from flask import flash, redirect, url_for, render_template, request
from datetime import datetime

from flask_notebook import app, db
from flask_notebook.models import DBNotes
from flask_notebook.forms import NewNoteForm, EditNoteForm


# global variable for the edit note function
note_id_list = []


@app.route('/', methods=['GET', 'POST'])
def index():
    # query the database for all notes
    all_notes = DBNotes.query.order_by(DBNotes.time_last_modify.desc()).all()

    # obtain the form
    form = NewNoteForm()

    if form.validate_on_submit():
        # get current time
        current = datetime.now()

        # obtain the body data
        body = form.body.data

        # build the record
        new_note_to_db = DBNotes(body=body, time_create=current, time_last_modify=current)
        db.session.add(new_note_to_db)
        db.session.commit()

        # render the page again
        # include the date and time

        flash('Successfully create a new note at {}'.format(current.strftime('%Y-%m-%d %H:%M')))
        return redirect(url_for('index'))

    # if the form is not submitted, simply display the form and all notes
    return render_template('index.html', form=form, all_notes=all_notes)


# only allow post method
@app.route('/edit_notes', methods=['POST'])
def edit_notes():
    # determine which button is pressed
    # page can be from the 'edit' and 'delete' button from the index page
    # or from the 'submit changes' from the edit_notes page

    if request.form.get('Edit'):
        # the user selects several notes from the index page to update
        # the user has submitted some updates, but maybe not all
        # print(request.form.getlist('select')):
        # query the database and get these notes into a list
        global note_id_list
        note_id_list = [int(str_id) for str_id in request.form.getlist('select')]
        edit_note_list = []
        form_list = []

        for note_id in note_id_list:
            this_note = DBNotes.query.get(note_id)
            this_form = EditNoteForm()
            this_form.body.label = note_id
            this_form.body.data = this_note.body

            edit_note_list.append(this_note)
            form_list.append(this_form)

        return render_template('edit_notes.html', edit_note_list=edit_note_list, form_list=form_list)

    elif request.form.get('Delete'):
        note_id_list_to_delete = [int(str_id) for str_id in request.form.getlist('select')]
        for note_id in note_id_list_to_delete:
            this_note =DBNotes.query.get(note_id)
            db.session.delete(this_note)
            db.session.commit()

        current = datetime.now()
        flash('Successfully delete {} notes at {}'.format(len(note_id_list_to_delete), current.strftime('%Y-%m-%d %H:%M')))
        return redirect(url_for('index'))

    elif request.form.get('Submit Changes'):
        # the user changes the form 'body' section
        # after press submit button, the final data is in request.form
        # in a form of immutable multi dict
        # use getlist to make to a list
        # the list should have same length as the note_id_list
        new_body_list = request.form.getlist('body')

        if len(new_body_list) != len(note_id_list):
            return 'Error'

        # get the modified time
        current = datetime.now()

        # count how many are changed
        count = 0

        for idx in range(len(note_id_list)):
            # extract the original note
            original_note = DBNotes.query.get(note_id_list[idx])
            # if the body data is updated
            if new_body_list[idx] != original_note.body:
                original_note.body = new_body_list[idx]
                original_note.time_last_modify = current
                db.session.commit()
                count += 1

        # delete all content in the note_id_list
        note_id_list = []

        if count != 0:
            flash('Successfully update {} notes at {}'.format(count, current.strftime('%Y-%m-%d %H:%M')))

        return redirect(url_for('index'))

    else:
        render_template('errors/404.html')

