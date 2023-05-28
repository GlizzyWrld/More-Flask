from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, TextAreaField, BooleanField
from wtforms.validators import  Length, InputRequired, URL,NumberRange, Optional


class PetAdd(FlaskForm):
    """Form for adding a pet"""
    name = StringField(
        "Pet Name",
        validators=[InputRequired()]
    )

    species = SelectField(
        "Species",
        choices=[('Hellcat', 'Hellcat'), ('Dog', 'Dog'), ('Porcupine', 'Porcupine'),]
    )

    photo_url = StringField(
        "Photo URL",
        validators=[URL(), Optional()]
    )

    age = IntegerField(
        "Age",
        validators=[Optional(), NumberRange(min=10, max=30)]
    )

    notes = TextAreaField(
        "Comments",
        validators=[Optional(), Length(min=10)]
    )

class PetEdit(FlaskForm):
    """For to edit a pet"""
    photo_url = StringField(
        "Photo URL",
        validators=[Optional(),URL()]
        )
    
    notes = TextAreaField(
        "Comments",
        validators=[Optional(), Length(min=10)]
    )

    available = BooleanField('Available??')




   