from datetime import datetime
from flask_notebook import db


# create a table DBNotes(id, body, timestamp)
class DBNotes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, default=datetime.now, index=True)


