#db has not been created yet, this is where we store data in the db
from flask_login import UserMixin
from . import db
from datetime import datetime

#users class
class User(db.Model, UserMixin):
    __tablename__='users' # good practice to specify table name
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True)
    emailid = db.Column(db.String(100), index=True, nullable=False, unique = True)
    #emailid = db.Column(db.String(100), index=True, primary_key=True)
	#password is never stored in the DB, an encrypted password is stored
	# the storage should be at least 255 chars long
    password_hash = db.Column(db.String(255), nullable=False)

    # relation to call user.comments and comment.created_by
    comments = db.relationship('Comment', backref='user')
    booking = db.relationship('Booking', backref='user')

#events class
class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    description = db.Column(db.String(200))
    image = db.Column(db.String(400))
    date = db.Column(db.String(20))
    venue = db.Column(db.String(80))
    price = db.Column(db.Numeric(8))
    quota = db.Column(db.Integer, default = 1)
    category = db.Column(db.String(20))
    # ... Create the Comments db.relationship
	# relation to call destination.comments and comment.destination
    comments = db.relationship('Comment', backref='events')
    booking = db.relationship('Booking', backref='events')
    # one to one relationship with event status
    event_status = db.relationship('Event_Status', backref="events")
    #event_status = db.relationship('Event_Status', backref="events")

    def __repr__(self): #string print method
        return "<Name: {}>".format(self.name)

#event_status class
class Event_Status(db.Model):
    __tablename__ = 'event_status'
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'),primary_key=True)
    status = db.Column(db.String(10))

    def __repr__(self):
        return "<Status: {}".format(self.status)

#comments class
class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(400))
    created_at = db.Column(db.DateTime, default=datetime.now())
    #add the foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    events_id = db.Column(db.Integer, db.ForeignKey('events.id'))


    def __repr__(self):
        return "<Comment: {}>".format(self.text)


#booking class
class Booking(db.Model):
    __tablename__ = 'booking'
    booking_Id = db.Column(db.Integer, primary_key=True)
    booking_date = db.Column(db.Date, default=datetime.now())
    price = db.Column(db.Integer)
    quantity = db.Column(db.Integer, default = 1)
    
    #foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    events_id = db.Column(db.Integer, db.ForeignKey('events.id'))