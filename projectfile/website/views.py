from flask import Blueprint, render_template, request, redirect,url_for, flash
from .models import Event

mainbp = Blueprint('main', __name__)
#create sqlite query to select each category, example rockCategory = Event.query.filter(Event.category.like("Rock")).all()
#this will create a list of events for each category 
#this query can be used any time we want to show events by category - can then take out the jinja2 if statement 
#which is calling the event variable which returns all of the events in the database
@mainbp.route('/')
def index():
    event = Event.query.all()
    #category = Event.query.filter(Event.category).all()
    rockEvent = Event.query.filter(Event.category.like("Rock")).all()
    popEvent = Event.query.filter(Event.category.like("Pop")).all()
    jazzEvent = Event.query.filter(Event.category.like("Jazz")).all()
    return render_template('index.html', event = event, rockEvent = rockEvent, popEvent = popEvent, jazzEvent = jazzEvent) #rockCategory = rockCategory then call in html jinja2 template in for loop

@mainbp.route('/search',  methods=['GET', 'POST'])
def search():
    if request.args['search']:
        print(request.args['search'])
        dest = "%" + request.args['search'] + '%'
        event = Event.query.filter(Event.description.like(dest)).all()
        return render_template('search.html', event=event)
    else:
        flash("No Results Found.")
        return redirect(url_for('main.index'))