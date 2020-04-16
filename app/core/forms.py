from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, \
    TextAreaField, FileField
from wtforms.validators import DataRequired,\
    ValidationError, Length
from app.models import User

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    bio = TextAreaField('Bio', validators=[Length(min=0, max=140)])
    photo = FileField('photo')
    submit = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if self.original_username != username.data:
            user = User.query.filter_by(username=username.data).first()
            if user is not None:
                raise ValidationError("Username is already taken!")


class PostForm(FlaskForm):
    post = TextAreaField('Say Something', validators=[
        DataRequired(),
        Length(min=1, max=140)
    ])
    submit = SubmitField("Submit")