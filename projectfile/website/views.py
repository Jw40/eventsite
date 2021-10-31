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

@mainbp.route('/category')
def category():
    event = Event.query.all()
    rockEvent = Event.query.filter(Event.category.like("Rock")).all()
    popEvent = Event.query.filter(Event.category.like("Pop")).all()
    jazzEvent = Event.query.filter(Event.category.like("Jazz")).all()
    countryEvent = Event.query.filter(Event.category.like("Country")).all()
    electronicEvent = Event.query.filter(Event.category.like("Electronic")).all()
    funkEvent = Event.query.filter(Event.category.like("Funk")).all()
    reggaeEvent = Event.query.filter(Event.category.like("Reggae")).all()
    heavyEvent = Event.query.filter(Event.category.like("Heavy Metal")).all()
    rythemEvent = Event.query.filter(Event.category.like("Rhythm and Blues")).all()
    return render_template('category.html', event = event, rockEvent = rockEvent, popEvent = popEvent, jazzEvent = jazzEvent, countryEvent = countryEvent, electronicEvent = electronicEvent,
    funkEvent = funkEvent, reggaeEvent = reggaeEvent, heavyEvent = heavyEvent, rythemEvent = rythemEvent) 

@mainbp.route('/search',  methods=['GET', 'POST'])
def search():
    if request.args['search']:
        print(request.args['search'])
        dest = "%" + request.args['search'] + '%'
        event = Event.query.filter(Event.description.like(dest)).all()
        flash(dest.replace("%",""), 'search_error')
        return render_template('search.html', event=event)
    else:
        flash("No Results Found.", 'search_error')
        return redirect(url_for('main.index'))

@mainbp.route('/help')
def help():
    return render_template('help.html') 

