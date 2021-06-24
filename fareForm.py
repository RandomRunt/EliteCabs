from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField
from wtforms.validators import ValidationError, data_required, input_required


class fareCalculator(FlaskForm):
    #tripDistance
    tripOrigin = StringField("Start address: ", validators=[data_required])
    tripDestination = StringField("Destination address: ", validators=[data_required])
    submit = SubmitField('OK')
