from app import db
from sqlalchemy.orm import relationship, backref

class Venue(db.Model):
    __tablename__ = "venues"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(280), index=True, unique=True, nullable=False)
    address = db.Column(db.String(280), index=True)
    lat = db.Column(db.String(280))
    lng = db.Column(db.String(280))

    artists = relationship("Artist", secondary="shows")

    def __repr__(self):
        return '<Venue {}>'.format(self.name)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'lat': self.lat,
            'lng': self.lng
        }

class Artist(db.Model):
    __tablename__ = "artists"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(280), index=True, unique=True, nullable=False)
    preview_video_url = db.Column(db.String(280))
    preview_video_thumbnail = db.Column(db.String(280))

    venues = relationship("Venue", secondary="shows")

    def __repr__(self):
        return '<Artist {}, {}, {}>'.format(self.name, self.preview_video_url, self.preview_video_thumbnail)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'preview_video_url': self.preview_video_url,
            'preview_video_thumbnail': self.preview_video_thumbnail
        }

class Show(db.Model):
    __tablename__ = "shows"
    id = db.Column(db.Integer, primary_key=True)
    venue_id = db.Column(db.Integer, db.ForeignKey("venues.id"), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey("artists.id"), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)

    artist = relationship(Artist, backref=backref("shows", cascade="all, delete-orphan"))
    venue = relationship(Venue, backref=backref("shows", cascade="all, delete-orphan"))
