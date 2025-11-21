from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    interactions = db.relationship('Interaction', backref='user', lazy=True)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(500))
    rating = db.Column(db.Float)
    reviews = db.Column(db.Integer, default=0)
    category = db.Column(db.String(100))
    description = db.Column(db.Text)
    source_site = db.Column(db.String(50))
    product_url = db.Column(db.String(500))

class Interaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=True) # Can be null for search
    type = db.Column(db.String(20), nullable=False) # 'view', 'search', 'click'
    metadata_json = db.Column(db.String(500)) # Store search query or other details
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
