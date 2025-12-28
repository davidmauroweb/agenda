from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, Email, EqualTo, Regexp, Optional
from wtforms import ValidationError
from modelos import Usuarios
# CLASES de Auth

class RegisterForm(FlaskForm):
    username = StringField(
        validators=[
            InputRequired(),
            Length(3, 20, message="El nombre debe tener entre 3 y 20 caracteres"),
            Regexp(
                "^[A-Za-z][A-Za-z0-9_.]*$",
                message="El nombre solo puede contener letras, números, puntos o guiones bajos"
            )
        ]
    )
    email = StringField(validators=[InputRequired(), Email(), Length(1, 64)])
    pwd = PasswordField(validators=[InputRequired(), Length(8, 72)])
    cpwd = PasswordField(
        validators=[
            InputRequired(),
            Length(8, 72),
            EqualTo("pwd", message="Las contraseñas deben coincidir")
        ]
    )

    def validate_email(self, email):
        if Usuarios.query.filter_by(email=email.data).first():
            raise ValidationError("El correo ya está registrado")

    def validate_username(self, username):
        if Usuarios.query.filter_by(username=username.data).first():
            raise ValidationError("El nombre de usuario ya está en uso")

class LoginForm(FlaskForm):
    email = StringField(validators=[InputRequired(), Email(), Length(1, 64)])
    pwd = PasswordField(validators=[InputRequired(), Length(8, 72)])
    username = StringField(validators=[Optional()])