"""Models for Cupcake app."""
from flask_sqlalchemy import SQLAlchemy

DEFAULT_IMAGE = 'https://tinyurl.com/demo-cupcake'

db = SQLAlchemy()

class Cupcake(db.Model):
    """Model for cupcake"""

    __tablename__ = 'cupcakes'

    id = db.Column(db.Integer, primary_key=True)
    flavor = db.Column(db.Text(100), nullable=False)
    size = db.Column(db.Text(100), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    image = db.Column(db.Text, default = DEFAULT_IMAGE)

    def to_dict(self):
        """Serialize cupcake info to a dictionary"""
        
        return {
            "id": self.id,
            "flavor": self.flavor,
            "size": self.size,
            "rating": self.rating,
            "image": self.image
        }      

   

def connect_db(app):
    """Connect database for Flask app"""

    db.app = app
    db.init_app(app)