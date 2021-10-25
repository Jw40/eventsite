from flask import Blueprint, render_template, request, redirect,url_for
from .models import Event

mainbp = Blueprint('main', __name__)

@mainbp.route('/')
def index():
    event = Event.query.all()
    category = Event.query.filter(Event.category).all()
    return render_template('index.html', event = event, category = category)

@mainbp.route('/search')
def search():
    if request.args['search']:
        print(request.args['search'])
        dest = "%" + request.args['search'] + '%'
        events = Event.query.filter(Event.description.like(dest)).all()
        return render_template('index.html', events=events)
    else:
        return redirect(url_for('main.index'))