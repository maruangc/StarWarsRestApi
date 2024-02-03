"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Favorite, Person, Planet
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# GET Users / Person  ---------------------------------------------------------
@app.route('/users', methods=['GET'])
def get_users():
    resp = Person.query.all()
    return jsonify({'users': [person.serialize() for person in resp]})

# GET Users / Favorites  ---------------------------------------------------------
@app.route('/users/favorites/<int:user_id>', methods=['GET'])
def get_user_favorites(user_id):
    resp = Favorite.query.filter_by(person_id = user_id)
    return jsonify({'favorites for': [favorite.serialize() for favorite in resp]})

# GET People -----------------------------------------------------------------
@app.route('/people', methods=['GET'])
def get_people():
    resp = Character.query.all()
    return jsonify({'character': [character.serialize() for character in resp]})

# GET People With ID----------------------------------------------------------
@app.route('/people/<int:people_id>', methods=['GET'])
def get_PeopleById(people_id):
    resp = Character.query.filter_by(id = people_id).one_or_none()

    if resp is None:
        return jsonify({'error': 'No encontrado'}),404

    return jsonify({'character': [resp.serialize()]}),201

# GET Planet------------------------------------------------------------------
@app.route('/planets', methods=['GET'])
def get_planets():
    resp = Planet.query.all()
    return jsonify({'planets': [planet.serialize() for planet in resp]})

# GET Planet with ID ---------------------------------------------------------
@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_PlanetById(planet_id):
    resp = Planet.query.filter_by(id = planet_id).one_or_none()

    if resp is None:
        return jsonify({'error': 'No encontrado'}),404

    return jsonify({'planet': [resp.serialize()]}),201

# POST Favorite People--------------------------------------------------------
@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_people_to_favorite(people_id):
        body=request.json
        user_id=body.get('user_id', None)
        resp = Person.query.filter_by(id = user_id).one_or_none()
        if resp is None:
            return 'user is not fount'
        resp = Character.query.filter_by(id = people_id).one_or_none()
        if resp is None:
            return 'character is not fount '        
        new_favorite=Favorite(person_id=user_id, character_id=people_id)
        db.session.add(new_favorite)
        try:
            db.session.commit()
            return 'Favorite created'
        except Exception as error:
            db.session.rollback()
            print("-*-*-*-* Error encontrado: ", error)
            return 'an error ocurred'

# POST Favorite Planet--------------------------------------------------------
@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_planet_to_favorite(planet_id):
        body=request.json
        user_id=body.get('user_id', None)
        resp = Person.query.filter_by(id = user_id).one_or_none()
        if resp is None:
            return 'user is not fount'
        resp = Planet.query.filter_by(id = planet_id).one_or_none()
        if resp is None:
            return 'planet is not found'
        new_favorite=Favorite(person_id=user_id, planet_id=planet_id)
        db.session.add(new_favorite)
        try:
            db.session.commit()
            return 'Favorite created'
        except Exception as error:
            db.session.rollback()
            print("-*-*-*- Error encontrado: ", error)
            return 'an error ocurred'
        
# DELETE Favorite Planet--------------------------------------------------------
@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_planet_from_favorite(planet_id):
        body=request.json
        user_id=body.get('user_id', None)
        resp = Person.query.filter_by(id = user_id).one_or_none()
        if resp is None:
            return 'user is not found'
       
        resp = Favorite.query.filter_by(person_id = user_id, planet_id = planet_id).all()
        if not resp:
            return 'planet is not found',404

        for resp_unit in resp:
            db.session.delete(resp_unit)

        try:
            db.session.commit()
            return 'Favorite DELETED',200
        except Exception as error:
            db.session.rollback()
            print('\\\ Error encontrado: /// ', error)
            return 'an error ocurred',404
        
# DELETE Favorite Character--------------------------------------------------------
@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_people_from_favorite(people_id):
        body=request.json
        user_id=body.get('user_id', None)
        resp = Person.query.filter_by(id = user_id).one_or_none()
        if resp is None:
            return 'user is not found'
       
        resp = Favorite.query.filter_by(person_id = user_id, character_id = people_id).all()
        if not resp:
            return 'character is not found',404

        for resp_unit in resp:
            db.session.delete(resp_unit)

        try:
            db.session.commit()
            return 'Favorite DELETED',200
        except Exception as error:
            db.session.rollback()
            print('\\\ Error encontrado: /// ', error)
            return 'an error ocurred',404
#-----------------------------------------------------------------
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
