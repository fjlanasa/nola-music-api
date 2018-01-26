from app import app, db
from app.models import Venue, Artist, Show
import click
import requests
import pdb
import time
import datetime
import os

@app.cli.command()
def artist_search():
    recent_shows = Show.query.filter(Show.date >= datetime.date.today() - datetime.timedelta(7)).all()
    for artist in [ show.artist for show in recent_shows if show.artist.preview_video_url == None ]:
        time.sleep(1)
        artist_url = "https://www.googleapis.com/youtube/v3/search?maxResults=1&part=snippet&type=video&q={}&key={}".format(artist.name.replace('+', ''), os.environ['GOOGLE_API_KEY'])
        artist_req = requests.get(artist_url)
        try:
            json = artist_req.json()
            if len(json['items']) > 0:
                artist.preview_video_url = "https://www.youtube.com/watch?v={}".format(json['items'][0]['id']['videoId'])
                artist.preview_video_thumbnail = json['items'][0]['snippet']['thumbnails']['medium']['url']
                db.session.commit()
                print()
                print('SUCCESS')
                print(artist)
            else:
                print()
                print(artist)
                print(artist_url)
        except Exception as inst:
            print(inst)
