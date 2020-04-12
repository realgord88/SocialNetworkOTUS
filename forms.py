from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField, IntegerField, SelectField
from wtforms.validators import DataRequired, Email, InputRequired, EqualTo, NumberRange, Length

gender_select = [('male', 'Мужчина'), ('2', 'Женщина')]


class RegisterForm(FlaskForm):
    username = StringField("Логин: ", validators=[DataRequired()])
    firstname = StringField("Имя: ", validators=[DataRequired()])
    lastname = StringField("Фамилия: ", validators=[DataRequired()])
    email = StringField("Почта: ", validators=[Email()])
    gender = SelectField("Пол: ", choices=gender_select)
    city = StringField("Город: ", validators=[DataRequired()])
    age = IntegerField("Возраст: ", validators=[NumberRange(min=1, max=100)])
    interest = TextAreaField("Интересы: ", validators=[DataRequired()])
    password = PasswordField("Пароль: ", [InputRequired(), EqualTo('confirm', message='Пароль не совпадает'), Length(min=8, max=64, message='Минимальная длина пароля - 8 символов')])
    confirm = PasswordField("Повторите пароль:")
    submit = SubmitField("Отправить")


class LoginForm(FlaskForm):
    username = StringField("Логин: ", validators=[DataRequired()])
    password = PasswordField("Пароль: ", validators=[DataRequired()])
    submit = SubmitField("Войти")


class SearchForm(FlaskForm):
    search = StringField("Введите поисковый запрос", validators=[DataRequired()])
    submit = SubmitField("Найти")


class AddFriendForm(FlaskForm):
    submit_add = SubmitField("Добавить в друзья")


class DeleteFriendForm(FlaskForm):
    submit_delete = SubmitField("Удалить из друзей")
