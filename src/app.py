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

#ENDPOINT lista de Todos los Usuarios-----------------------------------------------------------------------------------
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

# Endpoint POST para crear un nuevo usuario
@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    new_user = User(email=data['email'],
                    password=data['password'],
                    name=data['name'],
                    surname=data['surname'],
                    is_active=True)  # Asignar un valor predeterminado para is_active
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.serialize()), 201

# Endpoint DELETE para eliminar un usuario
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    favorites_global1 = FavoritesCharacters.query.filter_by(user_id=user_id).all()
    favorites_global2 = FavoritesPlanets.query.filter_by(user_id=user_id).all()
    favorites_global3 = FavoritesVehicles.query.filter_by(user_id=user_id).all()
    if user:
        for i in favorites_global1:
            db.session.delete(i)
        for i in favorites_global2:
            db.session.delete(i)
        for i in favorites_global3:
            db.session.delete(i)
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted successfully"}), 200
    else:
        return jsonify({"error": "User not found"}), 404

#ENDPOINT lista de Todos los Favoritos=['GET'])-----------------------------------------------------------------
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


#Endpoint Todos los Personajes------------------------------------------------------------------------------------------
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

#Endpoint Get one Character--------------------------------------------------------------------------------------------
@app.route('/people/<int:people_id>', methods=['GET'])
def get_one_people(people_id):
    # this is how you can use the Family datastructure by calling its methods
    character = Characters.query.get(people_id)
    if character is None:
        return jsonify({"msg": "No existe el personaje"}), 404
    return jsonify(character.serialize()), 200

@app.route('/characters', methods=['POST'])
def create_character():
    data = request.json
    new_character = Characters(name=data['name'],
                               age=data['age'],
                               height=data.get('height'))  # height es opcional, por lo que utilizamos get() para obtenerlo
    db.session.add(new_character)
    db.session.commit()
    return jsonify(new_character.serialize()), 201

# Endpoint DELETE para eliminar un personaje
@app.route('/characters/<int:character_id>', methods=['DELETE'])
def delete_character(character_id):
    character = Characters.query.get(character_id)
    favorites_characters = FavoritesCharacters.query.filter_by(characters_id=character_id).all()  
    if character:
        for i in favorites_characters:
            db.session.delete(i)
        db.session.delete(character)
        db.session.commit()
        return jsonify({"message": "Character deleted successfully"}), 200
    else:
        return jsonify({"error": "Character not found"}), 404


#Enpoint POST añadir personaje a favoritos--------------------------------------------------------------------------------          

@app.route('/favorites_characters', methods=['POST'])
def add_favorite_character():
    data = request.json
    new_favorite = FavoritesCharacters(user_id=data['user_id'], characters_id=data['character_id'])
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify(new_favorite.serialize()), 201

# Endpoint DELETE para eliminar un personaje favorito
@app.route('/favorites_characters/<int:favorite_id>', methods=['DELETE'])
def delete_favorite_character(favorite_id):
    favorite = FavoritesCharacters.query.get(favorite_id)
    if favorite:
        db.session.delete(favorite)
        db.session.commit()
        return jsonify({"message": "Favorite character deleted successfully"}), 200
    else:
        return jsonify({"error": "Favorite character not found"}), 404


#Endpoint ALL Planets--------------------------------------------------------------------------------------------------
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

#Endpoint Get one Planet-----------------------------------------------------------------------------
@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_one_planet(planet_id):
    # this is how you can use the Family datastructure by calling its methods
    planet = Planets.query.get(planet_id)
    if planet is None:
        return jsonify({"msg": "No existe el planeta"}), 404
    return jsonify(planet.serialize()), 200
    

# Endpoint POST para crear un nuevo planeta
@app.route('/planets', methods=['POST'])
def create_planet():
    data = request.json
    new_planet = Planets(name=data['name'],
                         climate=data['climate'],
                         population=data.get('population'))  # population es opcional, por lo que utilizamos get() para obtenerlo
    db.session.add(new_planet)
    db.session.commit()
    return jsonify(new_planet.serialize()), 201

# Endpoint POST para agregar un planeta favorito a un usuario
@app.route('/favorites_planets', methods=['POST'])
def add_favorite_planet():
    data = request.json
    new_favorite = FavoritesPlanets(user_id=data['user_id'], planets_id=data['planet_id'])
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify(new_favorite.serialize()), 201

# Endpoint DELETE para eliminar un planeta favorito
@app.route('/favorites_planets/<int:favorite_id>', methods=['DELETE'])
def delete_favorite_planet(favorite_id):
    favorite = FavoritesPlanets.query.get(favorite_id)
    if favorite:
        db.session.delete(favorite)
        db.session.commit()
        return jsonify({"message": "Favorite planet deleted successfully"}), 200
    else:
        return jsonify({"error": "Favorite planet not found"}), 404


# Endpoint DELETE para eliminar un planeta
@app.route('/planets/<int:planet_id>', methods=['DELETE'])
def delete_planet(planet_id):
    planet = Planets.query.get(planet_id)
    favorites_planets = FavoritesPlanets.query.filter_by(planets_id=planet_id).all()
    if planet: 
        for i in favorites_planets:
            db.session.delete(i)
        db.session.delete(planet)
        db.session.commit()
        return jsonify({"message": "Planet deleted successfully"}), 200
    else:
        return jsonify({"error": "Planet not found"}), 404


#Endpoint ALL Vehicles----------------------------------------------------------------------------------
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

#Endpoint Get one Vehicle--------------------------------------------------------------------------------
@app.route('/vehicles/<int:vehicle_id>', methods=['GET'])
def get_one_vehicle(vehicle_id):
    # this is how you can use the Family datastructure by calling its methods
    vehicle = Vehicles.query.get(vehicle_id)
    if vehicle is None:
        return jsonify({"msg": "No existe el vehiculo"}), 404
    return jsonify(vehicle.serialize()), 200


# Endpoint POST para agregar un vehículo favorito a un usuario
@app.route('/favorites_vehicles', methods=['POST'])
def add_favorite_vehicle():
    data = request.json
    new_favorite = FavoritesVehicles(user_id=data['user_id'], vehicles_id=data['vehicle_id'])
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify(new_favorite.serialize()), 201

# Endpoint DELETE para eliminar un vehículo
@app.route('/vehicles/<int:vehicle_id>', methods=['DELETE'])
def delete_vehicle(vehicle_id):
    vehicle = Vehicles.query.get(vehicle_id)
    favorites_vehicles = FavoritesVehicles.query.filter_by(vehicles_id=vehicle_id).all()  
    if vehicle:
        for i in favorites_vehicles:
            db.session.delete(i)
        db.session.delete(vehicle)
        db.session.commit()
        return jsonify({"message": "Vehicle deleted successfully"}), 200
    else:
        return jsonify({"error": "Vehicle not found"}), 404
    
# Endpoint DELETE para eliminar un vehículo favorito
@app.route('/favorites_vehicles/<int:favorite_id>', methods=['DELETE'])
def delete_favorite_vehicle(favorite_id):
    favorite = FavoritesVehicles.query.get(favorite_id)
    if favorite:
        db.session.delete(favorite)
        db.session.commit()
        return jsonify({"message": "Favorite vehicle deleted successfully"}), 200
    else:
        return jsonify({"error": "Favorite vehicle not found"}), 404


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)