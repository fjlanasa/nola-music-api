from app import app, db
from app.models import Venue, Artist, Show
import click

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Venue': Venue, 'Artist': Artist, 'Show': Show}
