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
from models import db, User, Characters, Planets, Vehicles, FavoritesCharacters, FavoritesPlanets, FavoritesVehicles
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

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

#ENDPOINT lista de Todos los Usuarios
@app.route('/users', methods=['GET'])
def get_all_users():

    query_results = User.query.all()
    results = list(map(lambda item: item.serialize(), query_results))
    # print(results)
    if results == []:
        return jsonify({"msg":"Empty"}), 404

    response_body = {
        "msg": "Ok",
        "result": results
    }

    return jsonify(response_body), 200


#ENDPOINT lista de Todos los Usuarios
@app.route('/users/favorites', methods=['GET'])
def get_user_favorites():
    favorite_character = FavoritesCharacters.query.all()
    character_favorite = list(map(lambda item: item.serialize(), favorite_character))

    favorite_planet = FavoritesPlanets.query.all()
    planet_favorite = list(map(lambda item: item.serialize(), favorite_planet))

    favorite_vehicle = FavoritesVehicles.query.all()
    vehicle_favorite = list(map(lambda item: item.serialize(), favorite_vehicle))

    if character_favorite == [] and planet_favorite == [] and vehicle_favorite == []:
        return jsonify({"msg":"Empty"}), 404  

    response_body = {
        "msg": "Ok",
        "result": [
            character_favorite, 
            planet_favorite, 
            vehicle_favorite
        ]
    }

    return jsonify(response_body), 200


#Endpoint Todos los Personajes
@app.route('/people', methods=['GET'])
def get_all_people():

    query_results = Characters.query.all()
    results = list(map(lambda item: item.serialize(), query_results))
    # print(results)
    if results == []:
        return jsonify({"msg":"Empty"}), 404

    response_body = {
        "msg": "Ok",
        "result": results
    }

    return jsonify(response_body), 200

#Endpoint Get one Character
@app.route('/people/<int:people_id>', methods=['GET'])
def get_one_people(people_id):
    # this is how you can use the Family datastructure by calling its methods
    character = Characters.query.get(people_id)
    if character is None:
        return jsonify({"msg": "No existe el personaje"}), 404
    return jsonify(character.serialize()), 200


#Endpoint ALL Planets
@app.route('/planets', methods=['GET'])
def get_all_planets():

    query_results = Planets.query.all()
    results = list(map(lambda item: item.serialize(), query_results))
    # print(results)
    if results == []:
        return jsonify({"msg":"Empty"}), 404

    response_body = {
        "msg": "Ok",
        "result": results
    }

    return jsonify(response_body), 200


#Endpoint Get one Planet
@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_one_planet(planet_id):
    # this is how you can use the Family datastructure by calling its methods
    planet = Planets.query.get(planet_id)
    if planet is None:
        return jsonify({"msg": "No existe el planeta"}), 404
    return jsonify(planet.serialize()), 200


#Endpoint ALL Vehicles
@app.route('/vehicles', methods=['GET'])
def get_all_vehicles():

    query_results = Vehicles.query.all()
    results = list(map(lambda item: item.serialize(), query_results))
    # print(results)
    if results == []:
        return jsonify({"msg":"Empty"}), 404

    response_body = {
        "msg": "Ok",
        "result": results
    }

    return jsonify(response_body), 200


#Endpoint Get one Vehicle
@app.route('/vehicles/<int:vehicle_id>', methods=['GET'])
def get_one_vehicle(vehicle_id):
    # this is how you can use the Family datastructure by calling its methods
    vehicle = Vehicles.query.get(vehicle_id)
    if vehicle is None:
        return jsonify({"msg": "No existe el vehiculo"}), 404
    return jsonify(vehicle.serialize()), 200



# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
