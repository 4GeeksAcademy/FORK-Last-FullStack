"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
# Si, para usar los endpoints IMPORTAR las Clases necesarias
from api.models import db, User, Todos
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
# Importar esto para el registro de una clave SEGURA
# Generar y tambien checkear ambos importantes y con usos diferentes
from werkzeug.security import generate_password_hash, check_password_hash
# os y b64encode para registrar el password de forma segura
import os
from base64 import b64encode
# Jwt required para verificar en los endpoints la entrada con token y get_jwt_identity para la linea 108 
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)

# Endppoint para el LOGIN del USUARIO
@api.route('/register', methods=['POST'])
def add_new_user():
    try:
        body = request.json

        # Para usar facilmente el Filter o Filter by, primero definimos
        email = body.get("email")
        name = body.get("name")
        password = body.get("password")

        if email is None or name is None or password is None: 
            return jsonify("Name, Email and Password is required"), 400
        else:
            # Dame el usuario completo si es true esta condicion
            user = User.query.filter_by(email=email).one_or_none()

            if user is not None:
                return jsonify("User already exists"), 400
            # Aqui agregamos el mega password, convertimos el password basico del usuario a uno seguro
            # Combinando b64 + generate_password_hash de werkzeug
            salt = b64encode(os.urandom(32)).decode("utf-8")
            # Se requiere un limite de caracteres altos 
            password = generate_password_hash(f"{password}{salt}")

            # Uso de variable user dinamico, como lo ves arriba (reasignacion)
            user = User()
            user.name = name
            user.email = email
            user.password = password # 
            user.salt = salt
            db.session.add(user)
            try:
                db.session.commit()
                return jsonify("user created sucessfully"), 201
            except Exception as error:
                return jsonify(f"Error: {error.args}"), 500

    except Exception as error:
        return jsonify(error.args)
   
# Endpoint para logear la cuenta registrada    
@api.route('/login', methods=['POST'])
def login():
    try:
        body = request.json
        email = body.get("email", None)
        password = body.get("password", None)

        if email is None or password is None:
            return jsonify("Email and Password is required"), 400
        else:
            
            user = User.query.filter_by(email=email).one_or_none()
            if user is None:
                return jsonify({"message" : "credenciales erradas"}), 400
            else:
                # Con esto comprobamos si el email y la contrasena son iguales a los almacenados anteriormente con el register
                if  check_password_hash(user.password, f"{password}{user.salt}"): #El orden tiene que ser el mismo que el anterior!
                    # Una vez registrado y ahora logeado exitosamente es hora de usar token para los 
                    # proximos inicios de sesion

                    # Lo que puede recibir el token de entrada y salida son objetos, uno o muchos

                    # Lo normal es que la unica info que necesitamos dentro del token y que esta pueda 
                    # viajar sin peligro contra ataques es... el ID 
                    # (Esta info es aparte del propio codigo del token
                    # y se usa para acceder a info y de un usuario como el ID y si, esto sera publico)
                    
                    # Este Id de mi identity es muy util 
                    token = create_access_token(identity=str(user.id)) #Cambiar siempre a STR 
                    return jsonify({
                        "token" : token, "current_user" : user.serializable()
                    })
                else:
                    return jsonify("Credenciales erradas"), 400   

    except Exception as error:
        return jsonify(f"Error {error}")
    

#Endpoint para agregar tarea al usuaario
@api.route('/todos', methods=['POST'])
@jwt_required()
def add_todo():
    
    try:
        body = request.json
        todos = Todos()
        user_id = get_jwt_identity()  # me devuelve el id del user por que asi se lo pase en identity = 

        if body.get("label") is None:
            return jsonify("Tu body debe conteneder un label"), 400
        
        if body.get("is_done") is None:
            return jsonify("Tu body debe conteneder un is_done"), 400
    
    
        todos.label = body['label'] 
        todos.is_done = body.get('is_done')
        # el ID que conecta la ID de todos con ID del user sera IGUAL a get_jwt_identity  (<ID del user>)
        todos.user_id = user_id
        db.session.add(todos)

        try:
            db.session.commit()
            return jsonify('Tarea guardada exitosamente'), 201
        except Exception as error:
            # En caso se guarde muchas tareas pero entre muchas  uno falla, se borra todo y no se guarda nada
            db.session.rollback()
            return jsonify(f"DEEP ERROR: {error.args}"), 500

    except Exception as error:
            return jsonify(f"ERROR {error.args}")


# Endpoint Consultar todas las tareas Todos de cierto usuario
@api.route('/todos', methods=['GET'])
@jwt_required()
def get_all_todos():
    try:
        # Similar al filter pero aqui busco el ID de get_jwt_identity
        todos = Todos.query.filter_by(user_id=get_jwt_identity()).all()
        print(todos)
        return jsonify("ok"), 200
    except Exception as error:
        return jsonify(f"ERROR {error.args}"), 500


