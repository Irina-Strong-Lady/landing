from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, SelectField,\
    SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, Regexp
from wtforms import ValidationError
from ..models import User, Claim
from wtforms_alchemy import PhoneNumberField

class ClaimEditForm(FlaskForm):
    name = StringField('Как к Вам обращаться?', validators=[Length(0, 64), Regexp(r'^[А-яа-яA-Za-z]+$', 0, 'Имя должно содержать только кириллицу либо латинские буквы без пробелов')], render_kw={'placeholder': 'Ваше имя'})
    email = StringField('Ваш Email', validators=[DataRequired(), Length(1, 64),
                                             Email()], render_kw={'placeholder': 'Email'})
    phone_number = PhoneNumberField('Ваш номер телефона', validators=[DataRequired()], region='RU',
                                    render_kw={'placeholder': '+7 (xxx) xxx-xx-xx (вводите цифры без пробелов)'})
    location = StringField('Ваш населенный пункт', validators=[Length(0, 64)], render_kw={'placeholder': 'Город, село (прочее)'})
    fabula = TextAreaField('Изложите Ваш вопрос', validators=[DataRequired()], render_kw={'placeholder': 'Введите текст здесь'})
    submit = SubmitField('Отправить заявку')