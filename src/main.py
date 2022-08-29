"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
# from crypt import methods
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planet, Favorites
# from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
db_url = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
    "postgres://", 'postgresql://')
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


# @app.route('/user', methods=['GET'])
# def handle_hello():

#     response_body = {
#         "msg": "Hello, this is your GET /user response "
#     }

#     return jsonify(response_body), 200


#ruta GET para todos los personajes y para traer personaje por id
#si funciona
@app.route('/people', methods=['GET'])
@app.route('/people/<int:people_id>', methods=['GET'])
def handle_people(people_id=None):
    if request.method == 'GET':
        if people_id == None:
            people = People()
            people = people.query.all()
            return jsonify(list(map(lambda item: item.serialize(), people)), 200)
        else:
            people = People()
            people = people.query.get(people_id)
            if people:
                return jsonify(people.serialize())

        return jsonify({"Not found"}), 404


#ruta GET para todos los planetas y para traer los planetas por id
#si funciona
@app.route('/planets', methods=['GET'])
@app.route('/planets/<int:planet_id>', methods=['GET'])
def handle_planet(planet_id=None):
    if request.method == 'GET':
        if planet_id == None:
            planet = Planet()
            planet = planet.query.all()
            return jsonify(list(map(lambda item: item.serialize(), planet)), 200)
        else:
            planet = Planet()
            planet = planet.query.get(planet_id)
            if planet:
                return jsonify(planet.serialize())

        return jsonify({"Not found"}), 404

#ruta GET para traer todos los usuarios
#si funciona
@app.route('/users', methods=['GET'])
def handle_user(user_id=None, nature=None, favorite_id=None):
    if request.method == 'GET':
        if user_id == None:
            user = User.query.all()
            return jsonify(list(map(lambda item: item.serialize(), user)), 200)
    return jsonify({"Not found"}),404


#si funciona, trae el usuario por su id
@app.route('/users/<int:user_id>', methods=['GET'])
def handle_user_id(user_id=None, nature=None, favorite_id=None):
    if request.method == 'GET':
        if user_id is not None:
            user=User()
            user=User.query.get(user_id)
            if user:
                return jsonify(user.serialize(), 200)
    return jsonify({"Not found"}),404




@app.route('/users/favorite', methods=['GET'])
def handle_user_favorite():
    if request.method == 'GET':
        favorites = Favorites()
        favorites=favorites.query.all()
        return jsonify(list(map(lambda items: items.serialize(), favorites))), 200

        

    return jsonify({"Not found"}),404








#ruta para hacer POST de un favorito

@app.route("/users/<int:user_id>/favorite", methods=['POST'])
def handle_favorite_post(user_id = None):
    if request.method == 'POST':
        user = User.query.get(user_id)
        if user is not None:

            body = request.json
            if body.get("name") is None:
                return jsonify({"message":"Error"}), 400
            elif body.get("nature_id") is None :
                return jsonify({"message":"Error"}), 400
            elif body.get("nature") is None :
                return jsonify({"message":"Error"}), 400
            another_fav= Favorites(name=body.get("name"), nature_id=body.get("nature_id"), nature=body.get("nature"),user_id=user_id)
            
            db.session.add(another_fav)

            try:
                db.session.commit()
                return jsonify(another_fav.serialize()), 201
            except Exception as error:
                print(error.args)
                db.session.rollback()
                return jsonify({"message": f"Error {error.args}"}), 500

#ruta para hacer DELETE de un favorito
# @app.route("/users/<int:user_id>/favorite", methods=['DELETE'])
# def handle_favorite_delete(user_id = None):
#     if request.method== 'DELETE':





# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)