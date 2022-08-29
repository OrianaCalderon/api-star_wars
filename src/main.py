"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from crypt import methods
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


#ruta GET para traer todos los usuarios y para traer los favoritos de el usuario por su id
@app.route('/users', methods=['GET'])
@app.route('/users/<int:user_id>/favorite', methods=['GET'])
def handle_user(user_id=None):
    if request.method == 'GET':
        if user_id == None:
            user = User()
            user = user.query.all()
            
            return jsonify(list(map(lambda item: item.serialize(), user)), 200)
        else: 
            favorites = Favorites()
            favorites = favorites.query.all()
            return jsonify(list(map(lambda items: items.serialize(), favorites)), 200)

    return jsonify({"Not found"}),404


#ruta para hacer POST de un favorito

#ruta para hacer DELETE de un favorito




# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
https://github.com/OrianaCalderon/api-star_wars