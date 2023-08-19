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
from models import db, User, Favorites, Planets, Characters, Starships
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

#TODOS LOS MÉTODOS DE USERS

@app.route('/user', methods=['GET'])
def get_users():
    users = User.query.all()
    users_serialized = list(map(lambda x: x.serialize(), users))
    response_body = {
        "msg": "Hello, this is your GET /user response",
        "users" : users_serialized
    }

    return jsonify(response_body), 200

@app.route('/user/<int:user_id>', methods=['GET'])
def get_single_user(user_id):
    single_user = User.query.get(user_id)
    if single_user is None:
        return jsonify({"msg": f"The id {user_id} user doesn't exist"}), 404
    
    response_body = {
        "msg": "Hello, this is your GET /user response ",
        "user_info" : single_user.serialize()
    }

    return jsonify(response_body), 200

@app.route('/user', methods=['POST'])
def post_user():
    body = request.get_json(silent=True)
    if body is None:
        raise APIException("You must send body information", status_code=400)
    
    if "username" not in body:
        raise APIException("You must send an username", status_code=404)

    if "email" not in body:
        raise APIException("You must send an email", status_code=404)
    
    if "password" not in body:
        raise APIException("You must send a password", status_code=404)
    print(body)

    new_user = User(username = body["username"], email = body["email"], password = body["password"], is_active = True)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg" : "User has been added successfully"}), 201


@app.route('/user', methods=['PUT'])
def modify_user():
    body = request.get_json(silent=True)
    if body is None:
        raise APIException("You must send body information", status_code=400)

    if "id" not in body:
        raise APIException("you must send the user id to be modified", status_code=404)
    
    if "username" not in body:
            raise APIException("You must send a new username or write the current one", status_code=404)
    
    if "email" not in body:
        raise APIException("You must send a new email or write the current one", status_code=404)
    
    single_users = User.query.get(body["id"])
    single_users.username = body["username"]
    single_users.email = body["email"]
    db.session.commit()
    return jsonify({"msg" : "User has been updated successfully"})

@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    single_user = User.query.get(user_id)
    if single_user is None:
        raise APIException("This user doesn't exist", status_code=400)
    db.session.delete(single_user)
    db.session.commit()
    return jsonify({"msg" : "User has been deleted successfully"})



#TODOS LOS MÉTODOS DE CHARACTERS

@app.route('/characters', methods=['GET'])
def get_characters():
    characters = Characters.query.all()
    characters_serialized = list(map(lambda x: x.serialize(), characters))
    response_body = {
        "msg": "Hello, this is your GET /characters response",
        "characters" : characters_serialized
    }

    return jsonify(response_body), 200

@app.route('/characters/<int:character_id>', methods=['GET'])
def get_single_character(character_id):
    single_character = Characters.query.get(character_id)
    if single_character is None:
        return jsonify({"msg": f"The id {character_id} user doesn't exist"}), 404
    
    response_body = {
        "msg": "Hello, this is your GET /single character response ",
        "character_info" : single_character.serialize()
    }

    return jsonify(response_body), 200

@app.route('/characters', methods=['POST'])
def post_character():
    body = request.get_json(silent=True)
    if body is None:
        raise APIException("You must send body information", status_code=400)
    
    if "character_name" not in body:
        raise APIException("You must send a character name", status_code=404)

    if "hair_color" not in body:
        raise APIException("You must send a hair color", status_code=404)
    
    if "height" not in body:
        raise APIException("You must send a height value", status_code=404)
    
    if "mass" not in body:
        raise APIException("You must send a mass value", status_code=404)

    if "skin_color" not in body:
        raise APIException("You must send a skin color", status_code=404)
    print(body)

    new_character = Characters(character_name = body["character_name"], hair_color = body["hair_color"], height = body["height"], mass = body["mass"], skin_color = body["skin_color"])
    db.session.add(new_character)
    db.session.commit()

    return jsonify({"msg" : "Character has been added successfully"}), 201


@app.route('/characters', methods=['PUT'])
def modify_character():
    body = request.get_json(silent=True)
    if body is None:
        raise APIException("You must send body information", status_code=400)

    if "character_name" not in body:
        raise APIException("You must send a new character name or write the current one", status_code=404)
    
    if "id" not in body:
        raise APIException("You must send the character id to be modified", status_code=404)
    
    if "hair_color" not in body:
        raise APIException("You must send a new hair color or write the current one", status_code=404)

    if "height" not in body:
        raise APIException("You must send an new height value or write the current one", status_code=404)

    if "mass" not in body:
        raise APIException("You must send a new mass value or write the current one", status_code=404)
    
    if "skin_color" not in body:
        raise APIException("You must send a new skin color or write the current one", status_code=404)
    
    single_character = Characters.query.get(body["id"])
    single_character.character_name = body["character_name"]
    single_character.hair_color = body["hair_color"]
    single_character.height = body["height"]
    single_character.mass = body["mass"]
    single_character.skin_color = body["skin_color"]
    db.session.commit()

    return jsonify({"msg" : "Character has been updated successfully"})


@app.route('/characters/<int:character_id>', methods=['DELETE'])
def delete_character(character_id):
    single_character = Characters.query.get(character_id)
    if single_character is None:
        raise APIException("This character doesn't exist", status_code=404)
    db.session.delete(single_character)
    db.session.commit()
    return jsonify({"msg" : "Character has been deleted successfully"})

#TODOS LOS MÉTODOS DE PLANETS

@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planets.query.all()
    planets_serialized = list(map(lambda x: x.serialize(), planets))
    response_body = {
        "msg": "Hello, this is your GET /planets response",
        "planets" : planets_serialized
    }

    return jsonify(response_body), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_single_planet(planet_id):
    single_planet = Planets.query.get(planet_id)
    if single_planet is None:
        return jsonify({"msg": f"The id {planet_id} planet doesn't exist"}), 404
    
    response_body = {
        "msg": "Hello, this is your GET /single planet response ",
        "planet_info" : single_planet.serialize()
    }

    return jsonify(response_body), 200

@app.route('/planets', methods=['POST'])
def post_planets():
    body = request.get_json(silent=True)
    if body is None:
        raise APIException("You must send body information", status_code=400)
    
    if "planet_name" not in body:
        raise APIException("You must send a planet name", status_code=404)

    if "gravity" not in body:
        raise APIException("You must send a gravity value", status_code=404)
    
    if "diameter" not in body:
        raise APIException("You must send a diameter value", status_code=404)
    
    if "rotation_period" not in body:
        raise APIException("You must send a rotation period value", status_code=404)

    print(body)

    new_planet = Planets(planet_name = body["planet_name"], gravity = body["gravity"], diameter = body["diameter"], rotation_period = body["rotation_period"])
    db.session.add(new_planet)
    db.session.commit()

    return jsonify({"msg" : "Planet has been added successfully"}), 201


@app.route('/planets', methods=['PUT'])
def modify_planets():
    body = request.get_json(silent=True)
    if body is None:
        raise APIException("You must send body information", status_code=400)
    
    if "id" not in body:
        raise APIException("You must send the planet id to be modified", status_code=404)

    if "planet_name" not in body:
        raise APIException("You must send a new planet name or write the current one", status_code=404)
    
    if "gravity" not in body:
        raise APIException("You must send a new gravity value or write the current one", status_code=404)

    if "diameter" not in body:
        raise APIException("You must send a new diameter value or write the current one", status_code=404)

    if "rotation_period" not in body:
        raise APIException("You must send a new rotation period value or write the current one", status_code=404)
    
    
    single_planet = Planets.query.get(body["id"])
    single_planet.planet_name = body["planet_name"]
    single_planet.gravity = body["gravity"]
    single_planet.diameter = body["diameter"]
    single_planet.rotation_period = body["rotation_period"]
    db.session.commit()

    return jsonify({"msg" : "Planet has been updated successfully"})


@app.route('/planets/<int:planet_id>', methods=['DELETE'])
def delete_planets(planet_id):
    single_planet = Planets.query.get(planet_id)
    if single_planet is None:
        raise APIException("This planet doesn't exist", status_code=400)
    db.session.delete(single_planet)
    db.session.commit()
    return jsonify({"msg" : "Planet has been deleted successfully"})


#TODOS LOS MÉTODOS DE STARSHIPS

@app.route('/starships', methods=['GET'])
def get_starships():
    starships = Starships.query.all()
    starships_serialized = list(map(lambda x: x.serialize(), starships))
    response_body = {
        "msg": "Hello, this is your GET /starships response",
        "starships" : starships_serialized
    }

    return jsonify(response_body), 200

@app.route('/starships/<int:starship_id>', methods=['GET'])
def get_single_starship(starship_id):
    single_starship = Starships.query.get(starship_id)
    if single_starship is None:
        return jsonify({"msg": f"The id {starship_id} starship doesn't exist"}), 404
    
    response_body = {
        "msg": "Hello, this is your GET /single starship response ",
        "starship_info" : single_starship.serialize()
    }

    return jsonify(response_body), 200

@app.route('/starships', methods=['POST'])
def post_starships():
    body = request.get_json(silent=True)
    if body is None:
        raise APIException("You must send body information", status_code=400)
    
    if "starship_name" not in body:
        raise APIException("You must send the starship name", status_code=404)

    if "model" not in body:
        raise APIException("You must send the starship model", status_code=404)
    
    if "starship_class" not in body:
        raise APIException("You must send the starship class", status_code=404)
    
    if "length" not in body:
        raise APIException("You must send the starship length value", status_code=404)
    
    if "crew" not in body:
        raise APIException("You must send the starship crew value", status_code=404)

    print(body)

    new_starship = Starships(starship_name = body["starship_name"], model = body["model"], starship_class = body["starship_class"], length = body["length"], crew = body["crew"])
    db.session.add(new_starship)
    db.session.commit()

    return jsonify({"msg" : "Starship has been added successfully"}), 201


@app.route('/starships', methods=['PUT'])
def modify_starships():
    body = request.get_json(silent=True)
    if body is None:
        raise APIException("You must send body information", status_code=404)
    
    if "id" not in body:
        raise APIException("you must send the starship id to be modified", status_code=404)
    
    if "starship_name" not in body:
        raise APIException("You must send the new starship name or write the current one", status_code=404)

    if "model" not in body:
        raise APIException("You must send the new starship model or write the current one", status_code=404)

    if "starship_class" not in body:
        raise APIException("You must send the new starship class or write the current one", status_code=404)

    if "length" not in body:
        raise APIException("You must send the new starship length value or write the current one", status_code=404)

    if "crew" not in body:
        raise APIException("You must send the new starship crew value or write the current one", status_code=404)

    single_character = Starships.query.get(body["id"])
    single_character.starship_name = body["starship_name"]
    single_character.model = body["model"]
    single_character.starship_class = body["starship_class"]
    single_character.length = body["length"]
    single_character.crew = body["crew"]

    db.session.commit()

    return jsonify({"msg" : "Starship has been updated successfully"})


@app.route('/starships/<int:starship_id>', methods=['DELETE'])
def delete_starships(starship_id):
    single_starship = Starships.query.get(starship_id)
    if single_starship is None:
        raise APIException(f"This starship {starship_id} doesn't exist", status_code=404)
    db.session.delete(single_starship)
    db.session.commit()
    return jsonify({"msg" : "Starship has been deleted successfully"})




#TODOS LOS MÉTODOS DE FAVORITES

@app.route('/favorites', methods=['GET'])
def get_favorites():
    favorites = Favorites.query.all()
    favorites_serialized = list(map(lambda x: x.serialize(), favorites))
    response_body = {
        "msg": "Hello, this is your GET /favorite lists response",
        "Favorite lists" : favorites_serialized
    }

    return jsonify(response_body), 200

@app.route('/favorites/<int:favorite_id>', methods=['GET'])
def get_single_favorite(favorite_id):
    single_favorite = Favorites.query.get(favorite_id)
    if single_favorite is None:
        return jsonify({"msg": f"The id {favorite_id} favorite list doesn't exist"}), 404
    
    response_body = {
        "msg": "Hello, this is your GET /favorite list response ",
        "favorite_list_info" : single_favorite.serialize()
    }

    return jsonify(response_body), 200

# ... (código anterior) ...
@app.route('/favorites', methods=['POST'])
def post_favorites():
    body = request.get_json(silent=True)
    if body is None:
        raise APIException("You must send body information", status_code=400)
    
    if "list_name" not in body:
        raise APIException("You must send a list name", status_code=400)
    
    if "character_id" not in body:
        raise APIException("You must send a character ID", status_code=400)

    if "planet_id" not in body:
        raise APIException("You must send a planet ID", status_code=400)
    
    if "starship_id" not in body:
        raise APIException("You must send a starship ID", status_code=400)

    new_favorite_list = Favorites(
        list_name=body["list_name"],
        character_id=body["character_id"],
        planet_id=body["planet_id"],
        starship_id=body["starship_id"]
    )

    db.session.add(new_favorite_list)
    db.session.commit()

    return jsonify({"msg": "Favorite list has been added successfully"}), 201

@app.route('/favorites/<int:favorite_id>', methods=['PUT'])
def update_favorite(favorite_id):
    favorite = Favorites.query.get(favorite_id)

    if favorite is None:
        return jsonify({"error": "Favorite not found"}), 404

    data = request.get_json()

    if 'list_name' in data:
        favorite.list_name = data['list_name']

    if 'planet' in data:
        new_planet = Planets.query.get(data['planet'])
        favorite.planets = new_planet


    if 'character' in data:
        new_character = Characters.query.get(data['character'])
        favorite.characters = new_character

    if 'starship' in data:
        new_starship = Starships.query.get(data['starship'])
        favorite.starships = new_starship

    db.session.commit()
    return jsonify({"msg": "Favorite updated successfully"}), 200



@app.route('/favorites/<int:favorite_id>', methods=['DELETE'])
def delete_favorite(favorite_id):
    favorite = Favorites.query.get(favorite_id)

    if favorite is None:
        return jsonify({"error": "Favorite not found"}), 404

    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"msg": "Favorite has been deleted successfully"}), 200

if __name__ == "__main__":
    app.run()



# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
