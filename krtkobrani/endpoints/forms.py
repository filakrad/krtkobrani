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


class GetHelp(FlaskForm):
    button_help = SubmitField('Nápověda')


class SubmitAnswer(FlaskForm):
    answer = StringField('Heslo')
    button_send = SubmitField('Odeslat')


class AddSite(FlaskForm):
    site_number = IntegerField("Číslo stanoviště")
    entry_pass = StringField('Heslo pro vstup')
    exit_pass = StringField('Heslo pro odchod')
    help_1_text = StringField('Text 1. nápovědy')
    help_1_time_minutes = IntegerField("Počet minut od příchodu k první nápovědě")
    help_2_text = StringField('Text 2. nápovědy')
    help_2_time_minutes = IntegerField("Počet minut od příchodu ke druhé nápovědě")
    dead_time_minutes = IntegerField("Počet minut od příchodu k deadu")
    next_site_location = StringField('Lokace dalšího stanoviště')
    button = SubmitField('Přidat')


class AddNews(FlaskForm):
    text = TextAreaField("Text novinky")
    button = SubmitField('Přidat')


class GameStart(FlaskForm):
    button = SubmitField('Začít hru')
