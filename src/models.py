import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Person(db.Model):
    __tablename__ = 'person'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(300), unique=False, nullable=False)
    name = db.Column(db.String(250), unique=False, nullable=False)
    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
        }


class Favorite(db.Model):
    __tablename__ = 'favorite'
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'))
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'))
    def serialize(self):
        return {
            "id": self.id,
            "person_id": self.person_id,
            "character_id": self.character_id,
            "planet_id": self.planet_id,
        }

class Character(db.Model):
    __tablename__ = 'character'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=False, nullable=False)
    height = db.Column(db.Integer, unique=False)
    mass = db.Column(db.Integer, unique=False)
    hair_color = db.Column(db.String(20), unique=False)
    skin_color = db.Column(db.String(20), unique=False)
    birth_year = db.Column(db.String(20), unique=False)
    gender = db.Column(db.String(20), unique=False)
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "mass": self.mass,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color,
            "birth_year": self.birth_year,
            "gender": self.gender,
        }

class Planet(db.Model):
    __tablename__ = 'planet'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=False, nullable=False)
    diameter = db.Column(db.Integer, unique=False)
    rotation_period = db.Column(db.Integer, unique=False)
    orbital_period = db.Column(db.Integer, unique=False)
    gravity = db.Column(db.String(50), unique=False)
    population = db.Column(db.Integer, unique=False)
    climate = db.Column(db.String(50), unique=False)
    terrain = db.Column(db.String(50), unique=False)
    surface_water = db.Column(db.Integer, unique=False)
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "diameter": self.diameter,
            "rotation_period": self.rotation_period,
            "orbital_period": self.orbital_period,
            "gravity": self.gravity,
            "population": self.population,
            "climate": self.climate,
            "terrain": self.terrain,
            "surface_water": self.surface_water,
        }


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }