from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    name = db.Column(db.String(250), nullable=False)
    surname = db.Column(db.String(250), nullable=False)
    subscripcion_date = db.Column(db.DateTime(), default=datetime.now())
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    favorite_character = db.relationship('FavoritesCharacters', backref='user', lazy=True)
    favorite_planet = db.relationship('FavoritesPlanets', backref='user', lazy=True)
    favorite_vehicle = db.relationship('FavoritesVehicles', backref='user', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "surname": self.name
            # do not serialize the password, its a security breach
        }

class Characters(db.Model):
    __tablename__ = 'characters'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    age = db.Column(db.String(80), unique=False, nullable=False)
    heigh = db.Column(db.Integer)
    favorites = db.relationship('FavoritesCharacters', backref='characters', lazy=True)

    def __repr__(self):
        return '<Characters %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "heigh": self.heigh
            # do not serialize the password, its a security breach
        }
    
class Planets(db.Model):
    __tablename__ = 'planets'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    climate = db.Column(db.String(250), nullable=False)
    population = db.Column(db.Integer)
    favorites = db.relationship('FavoritesPlanets', backref='planets', lazy=True)

    def __repr__(self):
        return '<Planets %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "population": self.population
            # do not serialize the password, its a security breach
        }
    

class Vehicles(db.Model):
    __tablename__ = 'vehicles'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    cargo = db.Column(db.Integer)
    passengers = db.Column(db.Integer)
    favorites = db.relationship('FavoritesVehicles', backref='vehicles', lazy=True)

    def __repr__(self):
        return '<Vehicles %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "cargo": self.cargo,
            "passengers": self.passengers
            # do not serialize the password, its a security breach
        }

class FavoritesCharacters(db.Model):
    __tablename__ = 'favorite_characters'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    characters_id = db.Column(db.Integer, db.ForeignKey('characters.id'))


    def __repr__(self):
        return '<FavoriteCharacters %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "characters_id": self.characters_id
            # do not serialize the password, its a security breach
        }

class FavoritesPlanets(db.Model):
    __tablename__ = 'favorite_planets'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    planets_id = db.Column(db.Integer, db.ForeignKey('planets.id'))

    def __repr__(self):
        return '<FavoritePlanets %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planets_id": self.planets_id
            # do not serialize the password, its a security breach
        }
    
class FavoritesVehicles(db.Model):
    __tablename__ = 'favorite_vehicles'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    vehicles_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'))

    def __repr__(self):
        return '<FavoriteVehicles %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "vehicles_id": self.vehicles_id
            # do not serialize the password, its a security breach
        }