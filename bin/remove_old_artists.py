from app import app, db
from app.models import Venue, Artist, Show
import click
from sqlalchemy import func

@app.cli.command()

def remove_old_artists():
    for artist in db.session.query(Artist).join(Show, isouter=True).group_by(Artist).having(func.count(Show.id) < 1):
        print(artist)
        db.session.delete(artist)

    db.session.commit()
    click.echo('done')
