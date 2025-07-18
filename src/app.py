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
from models import db, User, Niño, Digimon, Objeto, Favoritos
from sqlalchemy import select, and_
# from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
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

# @app.route('/user', methods=['GET'])
# def handle_hello():
#   response_body = {
#       "msg": "Hello, this is your GET /user response "
#    }
#   return jsonify(response_body), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)


# Aqui van mis rutas

# Rutas para los niños

@app.route('/niño', methods=['GET'])
def get_niños():
    stmt = select(Niño)
    niños = db.session.execute(stmt).scalars().all()

    return jsonify([niño.serialize() for niño in niños]), 200


@app.route('/niño/<int:id_nino>', methods=['GET'])
def get_one_kid(id_nino):
    stmt = select(Niño).where(Niño.id == id_nino)
    niño = db.session.execute(stmt).scalar_one_or_none()
    if niño is None:
        return jsonify({"Error": "Kid not found"}), 404
    return jsonify(niño.serialize()), 200


@app.route('/niño', methods=['POST'])
def create_kid():
    data = request.get_json()
    if not data or "nombre" not in data or "apellido" not in data or "edad" not in data:
        return jsonify({"Error": "Missing details"}), 400
    new_kid = Niño(
        nombre=data["nombre"],
        apellido=data["apellido"],
        edad=data["edad"],
        direccion=data["direccion"]
    )
    db.session.add(new_kid)
    db.session.commit()
    return jsonify(new_kid.serialize()), 201


@app.route('/niño/<int:id_nino>', methods=['PUT'])
def update_kid(id_nino):
    data = request.get_json()
    stmt = select(Niño).where(Niño.id == id_nino)
    niño = db.session.execute(stmt).scalar_one_or_none()
    if niño is None:
        return jsonify({"error": "Kid not found"}), 404
    niño.nombre = data.get("nombre", niño.nombre)
    niño.apellido = data.get("apellido", niño.apellido)
    niño.edad = data.get("edad", niño.edad)
    niño.direccion = data.get("direccion", niño.direccion)
    db.session.commit()
    return jsonify(niño.serialize()), 200


@app.route('/niño/<int:id_nino>', methods=['DELETE'])
def delete_kid(id_nino):
    stmt = select(Niño).where(Niño.id == id_nino)
    niño = db.session.execute(stmt).scalar_one_or_none()
    if niño is None:
        return jsonify({"error": "Kid not found"}), 404
    db.session.delete(niño)
    db.session.commit()
    return jsonify({"message": "Niño deleted"}), 200

# rutas para los digimons


@app.route('/digimon', methods=['GET'])
def get_digimons():
    stmt = select(Digimon)
    digimons = db.session.execute(stmt).scalars().all()

    return jsonify([digimon.serialize() for digimon in digimons]), 200


@app.route('/digimon/<int:id_digimon>', methods=['GET'])
def get_one_digimon(id_digimon):
    stmt = select(Digimon).where(Digimon.id == id_digimon)
    digimon = db.session.execute(stmt).scalar_one_or_none()
    if digimon is None:
        return jsonify({"Error": "digimon not found"}), 404
    return jsonify(digimon.serialize()), 200


@app.route('/digimon', methods=['POST'])
def create_digimon():
    data = request.get_json()
    if not data or "nombre" not in data or "tipo" not in data or "atributo" not in data or "altura" not in data or "peso" not in data:
        return jsonify({"Error": "Missing details"}), 400
    new_digimon = Digimon(
        nombre=data["nombre"],
        tipo=data["tipo"],
        atributo=data["atributo"],
        altura=data["altura"],
        peso=data["peso"]
    )
    db.session.add(new_digimon)
    db.session.commit()
    return jsonify(new_digimon.serialize()), 201


@app.route('/digimon/<int:id_digimon>', methods=['PUT'])
def update_digimon(id_digimon):
    data = request.get_json()
    stmt = select(Digimon).where(Digimon.id == id_digimon)
    digimon = db.session.execute(stmt).scalar_one_or_none()
    if digimon is None:
        return jsonify({"error": "Digimon not found"}), 404
    digimon.nombre = data.get("nombre", digimon.nombre)
    digimon.tipo = data.get("tipo", digimon.tipo)
    digimon.atributo = data.get("atributo", digimon.atributo)
    digimon.altura = data.get("altura", digimon.altura)
    digimon.peso = data.get("peso", digimon.peso)
    db.session.commit()
    return jsonify(digimon.serialize()), 200


@app.route('/digimon/<int:id_digimon>', methods=['DELETE'])
def delete_digimon(id_digimon):
    stmt = select(Digimon).where(Digimon.id == id_digimon)
    digimon = db.session.execute(stmt).scalar_one_or_none()
    if digimon is None:
        return jsonify({"error": "Digimon not found"}), 404
    db.session.delete(digimon)
    db.session.commit()
    return jsonify({"message": "Digimon deleted"}), 200

# Rutas para objetos


@app.route('/objeto', methods=['GET'])
def get_objetos():
    stmt = select(Objeto)
    objetos = db.session.execute(stmt).scalars().all()

    return jsonify([objeto.serialize() for objeto in objetos]), 200


@app.route('/objeto/<int:id_objeto>', methods=['GET'])
def get_one_objeto(id_objeto):
    stmt = select(Objeto).where(Objeto.id == id_objeto)
    objeto = db.session.execute(stmt).scalar_one_or_none()
    if objeto is None:
        return jsonify({"Error": "Object not found"}), 404
    return jsonify(objeto.serialize()), 200


@app.route('/objeto', methods=['POST'])
def create_object():
    data = request.get_json()
    if not data or "nombre" not in data or "color" not in data:
        return jsonify({"Error": "Missing details"}), 400
    new_object = Objeto(
        nombre=data["nombre"],
        color=data["color"],
    )
    db.session.add(new_object)
    db.session.commit()
    return jsonify(new_object.serialize()), 201


@app.route('/objeto/<int:id_objeto>', methods=['PUT'])
def update_objeto(id_objeto):
    data = request.get_json()
    stmt = select(Objeto).where(Objeto.id == id_objeto)
    objeto = db.session.execute(stmt).scalar_one_or_none()
    if objeto is None:
        return jsonify({"error": "Object not found"}), 404
    objeto.nombre = data.get("nombre", objeto.nombre)
    objeto.color = data.get("color", objeto.color)
    db.session.commit()
    return jsonify(objeto.serialize()), 200


@app.route('/objeto/<int:id_objeto>', methods=['DELETE'])
def delete_objeto(id_objeto):
    stmt = select(Objeto).where(Objeto.id == id_objeto)
    objeto = db.session.execute(stmt).scalar_one_or_none()
    if objeto is None:
        return jsonify({"error": "Object not found"}), 404
    db.session.delete(objeto)
    db.session.commit()
    return jsonify({"message": "Object deleted"}), 200

# Rutas para usuarios


@app.route('/user', methods=['GET'])
def get_users():
    stmt = select(User)
    users = db.session.execute(stmt).scalars().all()

    return jsonify([user.serialize() for user in users]), 200


@app.route('/user/<int:id_user>', methods=['GET'])
def get_one_user(id_user):
    stmt = select(User).where(User.id == id_user)
    user = db.session.execute(stmt).scalar_one_or_none()
    if user is None:
        return jsonify({"Error": "User not found"}), 404
    return jsonify(user.serialize()), 200


@app.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data or "email" not in data or "password" not in data:
        return jsonify({"Error": "Missing details"}), 400
    new_user = User(
        email=data["email"],
        password=data["password"],
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.serialize()), 201


@app.route('/user/<int:id_user>', methods=['PUT'])
def update_user(id_user):
    data = request.get_json()
    stmt = select(User).where(User.id == id_user)
    user = db.session.execute(stmt).scalar_one_or_none()
    if user is None:
        return jsonify({"error": "User not found"}), 404
    user.email = data.get("email", user.email)
    user.password = data.get("password", user.password)
    db.session.commit()
    return jsonify(user.serialize()), 200


@app.route('/user/<int:id_user>', methods=['DELETE'])
def delete_user(id_user):
    stmt = select(User).where(User.id == id_user)
    user = db.session.execute(stmt).scalar_one_or_none()
    if user is None:
        return jsonify({"error": "User not found"}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted"}), 200

# rutas para favoritos


@app.route('/favoritos', methods=['GET'])
def get_favorites():
    stmt = select(Favoritos)
    favoritos = db.session.execute(stmt).scalars().all()

    return jsonify([favorito.serialize() for favorito in favoritos]), 200


@app.route('/favoritos/<int:id_favorito>', methods=['GET'])
def get_one_favorite(id_favorito):
    stmt = select(Favoritos).where(Favoritos.id == id_favorito)
    favorito = db.session.execute(stmt).scalar_one_or_none()
    if favorito is None:
        return jsonify({"Error": "Favorites not found"}), 404
    return jsonify(favorito.serialize()), 200

# favoritos por user


@app.route('/user/<int:id_user>/favoritos', methods=['GET'])
def get_favorites_by_user(id_user):
    stmt = select(Favoritos).where(Favoritos.id_user == id_user)
    favoritos = db.session.execute(stmt).scalars().all()
    if not favoritos:
        return jsonify({"error": "No se encontro favoritos para este user"}), 404

    niños = []
    digimons = []
    objetos = []

    for fav in favoritos:
        if fav.id_niño:
            niños.append(fav.niño.serialize())
        if fav.id_digimon:
            digimons.append(fav.digimon.serialize())
        if fav.id_objeto:
            objetos.append(fav.objeto.serialize())

    return jsonify({
        "niños": niños,
        "digimons": digimons,
        "objetos": objetos
    }), 200

# Post fav niño


@app.route('/user/<int:user_id>/favoritos/niños', methods=['POST'])
def add_favorito_niño(user_id):
    data = request.get_json()
    id_niño = data.get("id_niño")
    if not id_niño:
        return jsonify({"error": "id_niño es requerido"}), 400

    if not User.query.get(user_id) or not Niño.query.get(id_niño):
        return jsonify({"error": "Usuario o Niño no encontrado"}), 404

    favorito = Favoritos(id_user=user_id, id_niño=id_niño)
    db.session.add(favorito)
    db.session.commit()
    return jsonify({"message": "Niño agregado a favoritos"}), 201

# post fav digimon


@app.route('/user/<int:user_id>/favoritos/digimons', methods=['POST'])
def add_favorito_digimon(user_id):
    data = request.get_json()
    id_digimon = data.get("id_digimon")
    if not id_digimon:
        return jsonify({"error": "id_digimon es requerido"}), 400

    if not User.query.get(user_id) or not Digimon.query.get(id_digimon):
        return jsonify({"error": "Usuario o Digimon no encontrado"}), 404

    favorito = Favoritos(id_user=user_id, id_digimon=id_digimon)
    db.session.add(favorito)
    db.session.commit()
    return jsonify({"message": "Digimon agregado a favorito"}), 201

# post Objeto favorito


@app.route('/user/<int:user_id>/favoritos/objetos', methods=['POST'])
def add_favorito_objeto(user_id):
    data = request.get_json()
    id_objeto = data.get("id_objeto")
    if not id_objeto:
        return jsonify({"error": "id_objeto es requerido"}), 400

    if not User.query.get(user_id) or not Objeto.query.get(id_objeto):
        return jsonify({"error": "Usuario o Objeto no encontrado"}), 404

    favorito = Favoritos(id_user=user_id, id_objeto=id_objeto)
    db.session.add(favorito)
    db.session.commit()
    return jsonify({"message": "Objeto agregado a favoritos"}), 201

# delete favorito niño


@app.route('/user/<int:user_id>/favoritos/niños/<int:id_nino>', methods=['DELETE'])
def delete_favorito_niño(user_id, id_nino):
    stmt = select(Favoritos).join(User, Favoritos.id_user == User.id).join(Niño, Favoritos.id_niño == Niño.id).where(and_(User.id == user_id, Niño.id == id_nino))
    favorito = db.session.execute(stmt).scalar_one_or_none()
    if favorito is None:
        return jsonify({"error": "Niño favorito no encontrado"}), 404

    db.session.delete(favorito)
    db.session.commit()
    return jsonify({"message": "Niño eliminado de favoritos"}), 200

# delete favorito digimon


@app.route('/user/<int:user_id>/favoritos/digimons/<int:id_digimon>', methods=['DELETE'])
def delete_favorito_digimon(user_id, id_digimon):
    stmt = select(Favoritos).join(User, Favoritos.id_user == User.id).join(Digimon, Favoritos.id_digimon == Digimon.id).where(and_(User.id == user_id, Digimon.id == id_digimon))
    favorito = db.session.execute(stmt).scalar_one_or_none()
    if favorito is None:
        return jsonify({"error": "Digimon favorito no encontrado"}), 404

    db.session.delete(favorito)
    db.session.commit()
    return jsonify({"message": "Digimon eliminado de favoritos"}), 200

# delete favortio objeto


@app.route('/user/<int:user_id>/favoritos/objetos/<int:id_objeto>', methods=['DELETE'])
def delete_favorito_objeto(user_id, id_objeto):
    stmt = select(Favoritos).join(User, Favoritos.id_user == User.id).join(Objeto, Favoritos.id_objeto == Objeto.id).where(and_(User.id == user_id, Objeto.id == id_objeto))
    favorito = db.session.execute(stmt).scalar_one_or_none()
    if favorito is None:
        return jsonify({"error": "Objeto Favorito no encontrado"}), 404

    db.session.delete(favorito)
    db.session.commit()
    return jsonify({"message": "Objeto eliminado de favoritos"}), 200
