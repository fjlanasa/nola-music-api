from app import app, db
from app.models import Venue, Artist, Show
import click
import requests
import datetime
import csv
from bs4 import BeautifulSoup
import os

@app.cli.command()
def seed_db():
    with open('shows.csv', newline='') as csvfile:
        showsreader = csv.DictReader(csvfile)
        for row in showsreader:
            venue_query = Venue.query.filter_by(name=row['venue']).first()
            if venue_query != None:
                venue_id = venue_query.id
            else:
                venue_name = row['venue'][:279]
                venue = { 'name': venue_name }
                place_req = requests.get("https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=29.9511,-90.0715&rankby=distance&keyword={}&key={}".format(venue_name, os.environ['GOOGLE_API_KEY']))
                try:
                    json = place_req.json()
                    venue['lat'] = json['results'][0]['geometry']['location']['lat']
                    venue['lng'] = json['results'][0]['geometry']['location']['lng']
                except Exception:
                    pass
                venue_model = Venue(**venue)
                db.session.add(venue_model)
                db.session.commit()
                venue_id = venue_model.id

            artist_query = Artist.query.filter_by(name=row['performer']).first()
            if artist_query != None:
                artist_id = artist_query.id
            else:
                artist_name = row['performer'][:279]
                artist = { 'name': artist_name }
                artist_req = requests.get("https://www.googleapis.com/youtube/v3/search?maxResults=1&part=snippet&type=video&q={}&key={}".format(artist_name, os.environ['GOOGLE_API_KEY']))
                try:
                    json = artist_req.json()
                    artist['preview_video_url'] = "https://www.youtube.com/watch?v={}".format(json['items'][0]['id']['videoId'])
                    artist['preview_video_thumbnail'] = json['items'][0]['snippet']['thumbnails']['medium']['url']
                except Exception:
                    pass
                artist_model = Artist(**artist)
                db.session.add(artist_model)
                db.session.commit()
                artist_id = artist_model.id

            date_arr = row['date'].split('-')
            year = int(date_arr[0])
            month = int(date_arr[1])
            day = int(date_arr[2])
            date_obj = datetime.date(year, month, day)

            time_arr = row['time'].split(':')
            hour = int(time_arr[0])
            minute = int(time_arr[1][:2])
            am_or_pm = time_arr[1][-2:]

            if am_or_pm == "pm":
                if hour < 12:
                    hour = hour + 12
                else:
                    hour = 0

            time_obj = datetime.time(hour, minute)

            show_model = Show(artist_id=artist_id, venue_id=venue_id, date=date_obj, time=time_obj)
            db.session.add(show_model)
            db.session.commit()
            print(row['date'])

    click.echo('hey!')
