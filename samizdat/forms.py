from wtforms import Form, StringField, EmailField, PasswordField, validators


class RegistrationForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = EmailField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('Password', [validators.Length(min=6, max=35)])


class LoginForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField('Password', [validators.Length(min=6, max=35)])


class EditorForm(Form):
    header = StringField('Header', [validators.Length(min=4, max=50)])
    content = StringField('Content', [validators.Length(min=1, max=3000)])
    # file = FileField('Image')
