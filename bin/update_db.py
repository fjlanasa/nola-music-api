from app import app, db
from app.models import Venue, Artist, Show
import click
import requests
import datetime
import csv
from bs4 import BeautifulSoup
import time
import os

@app.cli.command()
def update_db():
    date_obj = (datetime.date.today() + datetime.timedelta(7))
    date = date_obj.strftime('%Y-%m-%d')
    search_path = "https://www.wwoz.org/calendar/livewire-music?date={}".format(date)
    req = requests.get(search_path)
    page = req.text
    soup = BeautifulSoup(page, 'html.parser')

    music_events = []

    venues = soup.select(".livewire-listing .panel.panel-default")

    for v in venues:
        for listing in v.select(".row"):
            time.sleep(1)
            venue_name = v.select('.panel-title')[0].text.strip()[:279]
            artist_name = listing.select(".calendar-info p")[0].text.strip()[:279]
            time_arr = listing.select(".calendar-info p")[-1].text.strip().split(' ')[-1].split(":")

            venue_query = Venue.query.filter_by(name=venue_name).first()
            if venue_query != None:
                venue_id = venue_query.id
            else:
                venue_name = venue_name
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

            artist_query = Artist.query.filter_by(name=artist_name).first()
            if artist_query != None:
                artist_id = artist_query.id
            else:
                artist_name = artist_name
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
            print(date)

    click.echo('hey!')
