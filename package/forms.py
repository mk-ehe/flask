from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from package.models import User

class RegisterForm(FlaskForm):

    def validate_username(self, same_username):
        user = User.query.filter_by(username = same_username.data).first()
        if user:
            raise ValidationError("Username already taken! Try different Username.")
        
    def validate_email(self, same_email):
        email = User.query.filter_by(email = same_email.data).first()
        if email:
            raise ValidationError("Email is already linked to existing account.")
        

    username = StringField(label="Username", validators=[Length(min=3, max=30), DataRequired()])

    email = StringField(label="E-mail", validators=[Email(), DataRequired()])

    password = PasswordField(label="Password", validators=[Length(min=6), DataRequired()])

    confirm_password = PasswordField(label="Confirm Password", validators=[EqualTo("password"), DataRequired()])

    submit = SubmitField(label="Create Account")


class LoginForm(FlaskForm):

    username = StringField(label="Username:", validators=[DataRequired()])
    password = PasswordField(label="Password:", validators=[DataRequired()])
    submit = SubmitField(label="Sign in")