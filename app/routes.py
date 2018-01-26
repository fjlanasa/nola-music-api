from flask import jsonify
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
