from flask import jsonify, request
from app import app, models
from flask_cors import CORS
import datetime
import requests
import os

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
        try:
            filtered_shows = db_query.join(models.Show.venue).order_by(models.Venue.lat).all()

            url = "https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins={}&destinations=".format(location)
            for show in filtered_shows:
                if show.venue.lat != None:
                    url += "{},{}|".format(show.venue.lat, show.venue.lng)
            url = url[:-1] + "&key={}".format(os.environ["GOOGLE_API_KEY"])

            distance_matrix_request = requests.get(url)
            json = distance_matrix_request.json()
            for i, el in enumerate(json["rows"][0]["elements"]):
                filtered_shows[i].distance = el['distance']['value'] * 0.00062137
            filtered_shows = sorted(filtered_shows, key=lambda x: x.distance)

        except Exception as e:
            filtered_shows = db_query.all()
            pass
    else:
        filtered_shows = db_query.all()



    return jsonify(
        [ { 'artist': show.artist.serialize(),
            'venue': show.venue.serialize(),
            'date': show.date.strftime('%Y-%m-%d'),
            'time': show.time.strftime('%I:%M%p'),
            'distance': show.distance
           }
           for show in filtered_shows
        ]
    )
