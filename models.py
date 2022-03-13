"""Models for Cupcake app."""
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

default_url = "https://tinyurl.com/demo-cupcake"


class Cupcake(db.Model):
    """cupcake of cupcakely"""

    __tablename__ = "cupcakes"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    flavor = db.Column(db.Text, nullable=False)
    size = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Float)
    image = db.Column(db.Text, nullable=False, default=default_url)


def connect_db(app):
    """Connects to database."""

    db.app = app
    db.init_app(app)
