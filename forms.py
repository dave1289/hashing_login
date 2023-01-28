from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length

class UserForm(FlaskForm):

   username = StringField('Username',
                           validators=[InputRequired()])
   password = PasswordField('Password',
                           validators=[InputRequired(), Length(min=1, max=120)])

class TweetForm(FlaskForm):

   comment = StringField('Tweet',
                        validators=[InputRequired()])