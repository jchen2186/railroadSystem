from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email

class GetTrainsForm(FlaskForm):
    """
    Form for the front page. Used to filter or search for a train.
    """
    stations = [(1, 'Boston, MA - South Station'),
                (2, 'Boston, MA - Back Bay Station'),
                (3, 'Route 128, MA'),
                (4, 'Providence, RI'),
                (5, 'Kingston, RI'),
                (6, 'Westerly, RI'),
                (7, 'Mystic, CT'),
                (8, 'New London, CT'),
                (9, 'Old Saybrook, CT'),
                (10, 'New Haven, CT'),
                (11, 'Bridgeport, CT'),
                (12, 'Stamford, CT'),
                (13, 'New Rochelle, NY'),
                (14, 'New York, NY - Penn Station'),
                (15, 'Newark, NJ'),
                (16, 'Newark Libery Intl. Air., NJ'),
                (17, 'Metro Park, NJ'),
                (18, 'Trenton, NJ'),
                (19, 'Philadelphia, PA - 30th Street Station'),
                (20, 'Wilmington, DE - J.R. Biden, Jr. Station'),
                (21, 'Aberdeen, MD'),
                (22, 'Baltimore, MD - Penn Station'),
                (23, 'BWI Marshall Airport, MD'),
                (24, 'New Carrollton, MD'),
                (25, 'Washington, DC - Union Station')]

    date = DateField(label='Trip Date', id='date')
    station_start = SelectField(label='Start Station', choices=stations, id='station_start')
    station_end = SelectField(label='End Station', choices=stations, id='station_end')
    num_adult = StringField(label='Adult', id='num_adult')
    num_child = StringField(label='Child', id='num_child')
    num_senior = StringField(label='Senior', id='num_senior')
    num_military = StringField(label='Military', id='num_military')
    num_pets = StringField(label='Pets', id='num_pets')
    submit = SubmitField('Search for a train')

class ReservationForm(FlaskForm):
    email = StringField(label='Email Address', id='email',
                        validators=[DataRequired('Please enter an email address.'),
                                    Email(message='Please enter a valid email address.')])
    first_name = StringField(label='First name', id='first_name',
                             validators=[DataRequired('Please enter your first name.')])
    last_name = StringField(label='Last name', id='last_name',
                            validators=[DataRequired('Please enter your last name.')])
    credit_card = StringField(label='Credit Card Number', id='credit_card',
                              validators=[DataRequired('Please enter your credit card information.')])
    submit = SubmitField('Make Reservation')
