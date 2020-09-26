from flask import flash, redirect, url_for, render_template
from datetime import datetime

from flask_notebook import app, db
from flask_notebook.models import DBNotes
from flask_notebook.forms import NewNoteForm


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
