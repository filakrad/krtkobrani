from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, IntegerField, SubmitField, HiddenField
from wtforms import validators
from wtforms.validators import DataRequired


class Login(FlaskForm):
    email = StringField('email', validators=[DataRequired()])
    password = PasswordField('heslo', validators=[DataRequired()])
    submit = SubmitField("Přihlásit")


class PlayerForm(FlaskForm):
    name = StringField('Jméno')
    shirt_size = StringField('Číslo trička')
    sex = StringField('Pohlaví (M/F)')


class EditPlayerForm(PlayerForm):
    name = StringField('Jméno', validators=[DataRequired()])
    hidden_id = HiddenField()
    delete = SubmitField("Smazat hráče")


class AddPlayerForm(PlayerForm):
    submit = SubmitField("Vytvořit hráče")


class TeamForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    name = StringField('Jméno týmu', validators=[DataRequired()])
    four_digits = StringField('Unikátní čtyřciferné číslo', validators=[DataRequired()])
    phone = StringField('Kontaktní telefon', validators=[DataRequired()])
    car_type = StringField('Typ auta', validators=[DataRequired()])
    car_spz = StringField('Spz auta', validators=[DataRequired()])
    other_text = TextAreaField('Chcete nám něco napsat?')
    submit = SubmitField('Registrovat')


class RegistrationForm(TeamForm):
    password = StringField('Heslo', validators=[DataRequired()])


class EditTeamForm(TeamForm):
    password = StringField('Nové Heslo')
    submit = SubmitField('Uložit změny')


class AddPlayerButtonForm(FlaskForm):
    button = SubmitField('Přidat hráče')
