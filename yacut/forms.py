from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import URL, DataRequired, Length, Optional, Regexp

from yacut.constants import REG_EXPRESSION


class UrlForm(FlaskForm):
    original_link = URLField(
        "Оригинальная длинная ссылка",
        validators=[
            DataRequired(message="Обязательное поле"),
            URL(message="Некорректная ссылка"),
        ],
    )
    custom_id = StringField(
        "Пользовательский вариант короткой ссылки",
        validators=[
            Optional(),
            Length(max=16, message="Длина поля не должна превышать 16 символов."),
            Regexp(
                regex=REG_EXPRESSION,
                message='Допустимы только цифры и буквы "a-Z"',
            ),
        ],
    )
    submit = SubmitField("Создать")
