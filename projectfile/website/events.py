#routes to create and view events and view events comments, function to upload image file of event

#from the week 9 tutorial CHANGE code to events related stuff to create event with a image, route to event/comment


from flask import Blueprint, render_template, request, redirect, url_for,flash
from .models import Booking, Event, Comment, Event_Status
from .forms import EventForm, CommentForm, BookingHistoryForm, BookingForm, Status_List
from . import db
import os
from werkzeug.utils import secure_filename
#additional import:
from flask_login import login_required, current_user

bp = Blueprint('events', __name__, url_prefix='/events')

@bp.route('/<id>')
def show(id):
  event = Event.query.filter_by(id=id).first()
  # create the comment form
  bform = BookingForm()
  cform = CommentForm()    
  return render_template('events/show.html', event=event, cform=cform, bform=bform)

@bp.route('/create', methods = ['GET', 'POST'])
@login_required
def create():
  print('Method type: ', request.method)
  message = 'Sucessfully Created New Event.'
  form = EventForm()
  if form.validate_on_submit():
    #call the function that checks and returns image
    db_file_path=check_upload_file(form)
    event=Event(name=form.name.data, description=form.description.data, artist=form.artist.data,
    image=db_file_path, date=form.date.data, venue=form.venue.data, venue_address=form.venue_address.data, 
    city=form.city.data, state=form.state.data, zipcode=form.zipcode.data, price=form.price.data, 
    quota=form.ticket_num.data, category = form.category.data, owner = current_user.id) #this now works changed .id
    
    #event_obj = Event.query.filter_by(id=event).first()  
    
    # add the object to the db session
    db.session.add(event)
    db.session.commit()

    event_id = Event.query.filter_by(id=event.id).first().id  
    event_status =Event_Status(status = form.event_status.data, events_id =event_id)
    db.session.add(event_status)
    # commit to the database
    db.session.commit()
    print('Successfully created new event')
    flash(message)
    #Always end with redirect when form is valid
    return redirect(url_for('main.index'))
  print('not validate')
  return render_template('events/create.html', form=form)

def check_upload_file(form):
  #get file data from form  
  fp=form.image.data
  filename=fp.filename
  #get the current path of the module file… store image file relative to this path  
  BASE_PATH=os.path.dirname(__file__)
  #upload file location – directory of this file/static/image
  upload_path=os.path.join(BASE_PATH,'static/image',secure_filename(filename))
  #store relative path in DB as image location in HTML is relative
  db_upload_path='/static/image/' + secure_filename(filename)
  #save the file and return the db upload path  
  fp.save(upload_path)
  return db_upload_path

@bp.route('/<event>/comment', methods = ['GET', 'POST'])
@login_required  
def comment(event):  
    form = CommentForm()  
    #get the event object associated to the page and the comment
    event_obj = Event.query.filter_by(id=event).first()  
    if form.validate_on_submit():  
      #read the comment from the form
      comment = Comment(text=form.text.data,  
                        events=event_obj, 
                        user = current_user) 
      #here the back-referencing works - comment.event is set
      # and the link is created
      db.session.add(comment) 
      db.session.commit() 

      #flashing a message which needs to be handled by the html
      #flash('Your comment has been added', 'success')  
      print('Your comment has been added') 
    # using redirect sends a GET request to event.show
    return redirect(url_for('events.show', id=event))

@bp.route('/<event>/booking', methods = ['GET', 'POST'])
@login_required
def booking(event):
  form1 = BookingForm()
  #get the event object associated to the page
  event_obj = Event.query.filter_by(id=event).first()
  if form1.validate_on_submit():
    #get the booking details from the modal form
    booking = Booking(quantity = form1.quantity.data,
                      user_id = current_user.id,
                      price = form1.quantity.data,
                      events_id = event_obj.id)

    db.session.add(booking)
    db.session.commit()
    print('Successfully Booked!')
    return redirect(url_for('events.show', id=event))
  else:
    print('Failed to Book')
    return redirect(url_for('events.show', id=event))

@bp.route('/booking_history', methods = ['GET', 'POST'])
@login_required
def booking_history():
  records = db.session.query(Booking, Event).filter(Booking.events_id == Event.id).filter_by(user_id=current_user.id)
  return render_template('events/booking_history.html', records = records)



#place categroy find in when viewing place if 