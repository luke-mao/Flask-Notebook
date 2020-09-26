from flask import flash, redirect, url_for, render_template, request
from datetime import datetime

from flask_notebook import app, db
from flask_notebook.models import DBNotes
from flask_notebook.forms import NewNoteForm, EditNoteForm


@app.route('/', methods=['GET', 'POST'])
def index():
    # query the database for all notes
    all_notes = DBNotes.query.order_by(DBNotes.time_last_modify.desc()).all()

    # obtain the form
    form = NewNoteForm()

    if form.validate_on_submit():
        # obtain the body data
        body = form.body.data

        # build the record
        new_note_to_db = DBNotes(body=body)
        db.session.add(new_note_to_db)
        db.session.commit()

        # render the page again
        # include the date and time
        current = datetime.now()
        flash(
            'Your new note have been successfully recorded at {} {}:{}'.format(
                current.date(), current.hour, current.minute
            )
        )
        return redirect(url_for('index'))

    # if the form is not submitted, simply display the form and all notes
    return render_template('index.html', form=form, all_notes=all_notes)


@app.route('/edit_notes', methods=['GET', 'POST'])
def edit_notes():
    # the selected note.id is in the request.form.getlist('select')
    # print(request.form.getlist('select'))

    # print(request.method)
    #
    # if request.form.getlist('select'):
    #     # chosen something to edit
    #     print(request.form.getlist('select'))
    # else:
    #     print('no')
    #
    # return 'hello'

    if request.form.getlist('select'):
        # query the database and get these notes into a list
        edit_note_list = []
        form_list = []

        for note_id in request.form.getlist('select'):
            this_note = DBNotes.query.get(int(note_id))
            this_form = EditNoteForm()
            this_form.body.data = this_note.body

            edit_note_list.append(this_note)
            form_list.append(this_form)

        return render_template('edit_notes.html', edit_note_list=edit_note_list, form_list=form_list)

    else:
        return 'hello'

