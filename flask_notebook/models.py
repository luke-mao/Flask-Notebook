from datetime import datetime
from flask_notebook import db


# create a table DBNotes(id, body, timestamp)
class DBNotes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(200))

    # since we can modify the note
    # so create two columns: creation time and last modified time
    # during creation, both time are the same

    time_create = db.Column(db.DateTime)
    time_last_modify = db.Column(db.DateTime, index=True)


