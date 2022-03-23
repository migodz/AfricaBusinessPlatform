from wtforms import Form, StringField, EmailField, ValidationError
from wtforms.validators import Length, Regexp, Email
from models import User


class SignupForm(Form):
    usr = StringField(validators=[Length(min=5, max=25)])
    pwd = StringField(validators=[Regexp(r"^(?=.*[A-Za-z])(?=.*\d).{8,40}$")])
    email = EmailField(validators=[Email()])
    nknm = StringField(validators=[Length(min=5, max=25)])
    type = StringField(validators=[Length(min=3, max=3)])

    def validate_usr(self, field):
        usr_data = field.data
        res = User.query.filter_by(username=usr_data).first()
        if res:
            raise ValidationError("username already exists!")

    def validate_email(self, field):
        email_data = field.data
        res = User.query.filter_by(email=email_data).first()
        if res:
            raise ValidationError("email already exists!")

    def validate_type(self, field):
        type_data = field.data
        if not type_data in ('usr', 'cpn', 'cbr'):
            raise ValidationError("unknown user type!")


class LoginForm(Form):
    usr = StringField(validators=[Length(min=5, max=25)])
    pwd = StringField(validators=[Regexp(r"^(?=.*[A-Za-z])(?=.*\d).{8,40}$")])


class NewPasswordForm(Form):
    pwd = StringField(validators=[Regexp(r"^(?=.*[A-Za-z])(?=.*\d).{8,40}$")])
    new_pwd = StringField(validators=[Regexp(r"^(?=.*[A-Za-z])(?=.*\d).{8,40}$")])


class EmailForm(Form):
    email = EmailField(validators=[Email()])