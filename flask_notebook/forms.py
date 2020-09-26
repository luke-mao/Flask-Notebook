# create the forms


from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class NewNoteForm(FlaskForm):
    body = TextAreaField(label='New_Note', validators=[DataRequired(), Length(1, 200)])
    submit = SubmitField()      # submit button: no need for label


class EditNoteForm(FlaskForm):
    body = TextAreaField(validators=[DataRequired(), Length(1, 200)])
    submit = SubmitField()


