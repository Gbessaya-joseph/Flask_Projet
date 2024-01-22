from wtforms import Form, BooleanField, DateTimeField, TextAreaField, StringField
from wtforms.validators import Length, DataRequired

class AppointmentForm(Form):
    title = StringField('Title', validators=[Length(max=255)])
    start = DateTimeField('Start', validators=[DataRequired()])
    end = DateTimeField('End')
    allday = BooleanField('All Day')
    location = StringField('Location', validators=[Length(max=255)])
    description = TextAreaField('Description')