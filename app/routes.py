from flask import jsonify, request
from app import app, models
from flask_cors import CORS
import datetime

CORS(app)

@app.route('/')
@app.route('/index')
def index():
    todays_shows = models.Show.query.filter_by(date=datetime.date.today()).all()
    return jsonify(
        [ { 'artist': show.artist.serialize(),
            'venue': show.venue.serialize(),
            'date': show.date.strftime('%Y-%m-%d'),
            'time': show.time.strftime('%I:%M%p')
           }
           for show in todays_shows
        ]
    )

@app.route('/search')
@app.route('/search')
def search():
    date = request.args.get('date')
    time = request.args.get('time')
    location = request.args.get('location')
    db_query = None

    if date != None:
        year, month, day = date.split('-')
        date_obj = datetime.date(int(year), int(month), int(day))
        db_query = models.Show.query.filter_by(date=date_obj)
    else:
        db_query = models.Show.query.filter_by(date=datetime.date.today())

    if time != None:
        hour, minute = time.split(':')
        time_obj= datetime.time(int(hour), int(minute))
        db_query = db_query.filter_by(time=time_obj)

    if location != None:
        pass

    filtered_shows = db_query.all()

    return jsonify(
        [ { 'artist': show.artist.serialize(),
            'venue': show.venue.serialize(),
            'date': show.date.strftime('%Y-%m-%d'),
            'time': show.time.strftime('%I:%M%p')
           }
           for show in filtered_shows
        ]
    )
