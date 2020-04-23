from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, url, EqualTo, ValidationError, Email
from wtforms.widgets.html5 import NumberInput


class SetupForm(FlaskForm):
    mail_server= StringField("Mail SMTP Server", default="smtp.googlemail.com", validators=[DataRequired()])
    mail_port = IntegerField("Mail SMTP Port", widget=NumberInput(), default=587, validators=[DataRequired()])
    mail_use_tls = BooleanField("Use TLS for SMTP?", default=True)
    mail_username = StringField('Mail Username', validators=[DataRequired(), Email()])
    mail_password = PasswordField('Mail Password', validators=[DataRequired()])
    secret_key = StringField("Secret Key (Make this secure!)", validators=[DataRequired()])
    admin_email = StringField("Admin Email", validators=[DataRequired(), Email()])
    pusher_app_id = StringField("Pusher App ID", validators=[DataRequired()])
    pusher_key = StringField("Pusher Key", validators=[DataRequired()])
    pusher_secret = StringField("Pusher Secret", validators=[DataRequired()])
    pusher_cluster = StringField("Pusher Cluster", validators=[DataRequired()])
    submit = SubmitField("Submit")
