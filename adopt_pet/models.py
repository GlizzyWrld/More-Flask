from flask_sqlalchemy import SQLAlchemy

GENERIC_IMAGE = 'https://svg.template.creately.com/MIQyt1kde0t'

db = SQLAlchemy()

class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    species = db.Column(db.String(100), nullable=False)
    photo_url = db.Column(db.Text)
    age = db.Column(db.Integer)
    notes = db.Column(db.Text)
    available = db.Column(db.Boolean, nullable=False, default=True)

    def image_url(self):
        """Return image for pet -- bespoke or generic."""

        return self.photo_url or GENERIC_IMAGE


    def __repr__(self):
        return f'<Pet {self.id}: {self.name}>'

def connect_db(app):
    """Connect database for Flask app"""

    db.app = app
    db.init_app(app)