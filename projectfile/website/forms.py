#differnt type of forms using Wtfforms, login, register, eventform, comment form

from flask_wtf import FlaskForm
from wtforms.fields import DateField, TextAreaField,SubmitField, StringField, PasswordField, IntegerField
from wtforms.fields.core import SelectField
from wtforms.validators import InputRequired, Length, Email, EqualTo
from flask_wtf.file import FileRequired, FileField, FileAllowed

Categories_List = ('Rock', 'Pop', 'Jazz', 'Country','Electronic', 'Funk', 'Reggae', 'Heavy Metal', 'Rhythm and Blues')
Status_List = ('Upcoming', 'Booked', 'Canceled', 'Inactive')
Ages_List = ('All Ages', '18+ Only')

#creates the login information
class LoginForm(FlaskForm):
    user_name=StringField("User Name", validators=[InputRequired('Enter user name')])
    password=PasswordField("Password", validators=[InputRequired('Enter user password')])
    submit = SubmitField("Login")

 # this is the registration form
class RegisterForm(FlaskForm):
    user_name=StringField("User Name", validators=[InputRequired()])
    email_id = StringField("Email Address", validators=[Email("Please enter a valid email")])
    
    #add buyer/seller - check if it is a buyer or seller hint : Use RequiredIf field


    #linking two fields - password should be equal to data entered in confirm
    password=PasswordField("Password", validators=[InputRequired(),
                  EqualTo('confirm', message="Passwords should match")])
    confirm = PasswordField("Confirm Password")

    #submit button
    submit = SubmitField("Register")

#create EventForm
ALLOWED_FILE = {'PNG','JPG','png','jpg'}

#Create new event
class EventForm(FlaskForm):
  name = StringField('Event Name', validators=[InputRequired()])
  artist = StringField('Artist(s)', validators=[InputRequired()])
  date = DateField('Event Date', validators=[InputRequired()])
  venue = StringField('Venue Name', validators=[InputRequired()])
  venue_address = StringField('Venue Address', validators=[InputRequired()])
  city = StringField('City', validators=[InputRequired()])
  state = StringField('State', validators=[InputRequired()])
  zipcode = IntegerField('Zip Code', validators=[InputRequired()])
  
  ages = SelectField('Age Limit', choices=[(ages, ages) for ages in Ages_List], validators=[InputRequired()])
  category = SelectField('Category', choices=[(category, category) for category in Categories_List], validators=[InputRequired()])
  #category = StringField('Category', validators=[InputRequired()])
  event_status = SelectField('Status', choices=[(status, status) for status in Status_List], validators=[InputRequired()])
  #event_status = StringField('Status', validators=[InputRequired()])
  description = TextAreaField('Description', 
            validators=[InputRequired()])
  price = IntegerField('Ticket Price', validators=[InputRequired()])
  ticket_num = IntegerField('Ticket Quantity', validators=[InputRequired()])
  image = FileField('Event Image', validators=[
    FileRequired(message='Image cannot be empty'),
    FileAllowed(ALLOWED_FILE, message='Only supports png,jpg,JPG,PNG')])
  submit = SubmitField('Create')

#create BookingForm
class BookingForm(FlaskForm):
  quantity = IntegerField('Quantity', validators=[InputRequired()])
  submit = SubmitField('Book tickets')

#create CommentForm
#User comment
class CommentForm(FlaskForm):
  text = TextAreaField('Comment', [InputRequired()])
  submit = SubmitField('Create')

#create BookingForm

#create BookingHistoryForm
class BookingHistoryForm(FlaskForm):
  id = IntegerField('Ticket Price', validators=[InputRequired()])
  name = StringField(u'Event Name', validators=[InputRequired()])
  image = FileField('Event Image', validators=[
    FileRequired(message='Image cannot be empty'),
    FileAllowed(ALLOWED_FILE, message='Only supports png,jpg,JPG,PNG')])
  venue = StringField('Venue', validators=[InputRequired()])
  bookingdate = DateField('Booking Date', validators=[InputRequired()])
  date = DateField('Date', validators=[InputRequired()])
  ticket_num = IntegerField('Ticket Quantity', validators=[InputRequired()])
  price = IntegerField('Ticket Price', validators=[InputRequired()])
  submit = SubmitField("View Event Details")
