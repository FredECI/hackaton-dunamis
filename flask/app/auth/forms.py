from wtforms import Form, EmailField, PasswordField, validators, SubmitField, StringField


class LoginForm(Form):
    email = EmailField("Email", [validators.DataRequired()])
    senha = PasswordField("Senha", [validators.DataRequired()])
    botao = SubmitField("Login")


class RegisterForm(Form):
    nome = StringField("Nome", [validators.DataRequired()])
    email = EmailField("Email", [validators.DataRequired()])
    senha = PasswordField("Senha", [validators.DataRequired()])
    repita = PasswordField("Repita a senha", [validators.DataRequired()])
    botao = SubmitField("Login")
