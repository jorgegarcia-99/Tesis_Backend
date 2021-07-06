from bson.json_util import dumps, ObjectId
from flask import current_app
import azure.cosmos.documents as documents
import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.exceptions as exceptions
from azure.cosmos.partition_key import PartitionKey
# from pymongo import MongoClient, DESCENDING
from werkzeug.local import LocalProxy


# Este método se encarga de configurar la conexión con la base de datos
def get_db():
    HOST = current_app.config['HOST']
    MASTER_KEY = current_app.config['MASTER_KEY']
    DATABASE_ID = current_app.config['DATABASE_ID']

    client = cosmos_client.CosmosClient(HOST, {'masterKey': MASTER_KEY}, user_agent="CosmosDBPythonQuickstart", user_agent_overwrite=True)
    db = client.get_database_client(DATABASE_ID)

    return db

# def get_container_pub(db):
#     container_Publication = db.get_container_client("Publications")
#     return container_Publication

# def get_container_com(db):
#     container_Comment = db.get_container_client("Comments")
#     return container_Comment

# Use LocalProxy to read the global db instance with just `db`
db = LocalProxy(get_db)
# container_pub = LocalProxy(get_container_pub(db))
# container_com = LocalProxy(get_container_com(db))

def test_connection():
    return dumps(db.collection_names())


def collection_stats(collection_nombre):
    return dumps(db.command('collstats', collection_nombre))

# # -----------------Carreras-------------------------


# def crear_carrera(json):
#     return str(db.carreras.insert_one(json).inserted_id)


# def consultar_carrera_por_id(carrera_id):
#     return dumps(db.carreras.find_one({'_id': ObjectId(carrera_id)}))


# def actualizar_carrera(carrera):
#     # Esta funcion solamente actualiza nombre y descripcion de la carrera
#     return str(db.carreras.update_one({'_id': ObjectId(carrera['_id'])},
#                            {'$set': {'nombre': carrera['nombre'], 'descripcion': carrera['descripcion']}})
#                .modified_count)


# def borrar_carrera_por_id(carrera_id):
#     return str(db.carreras.delete_one({'_id': ObjectId(carrera_id)}).deleted_count)


# # Clase de operadores
# def consultar_carreras(skip, limit):
#     return dumps(db.carreras.find({}).skip(int(skip)).limit(int(limit)))


# def agregar_curso(json):
#     return str('Flata por implementar')

# def borrar_curso_de_carrera(json):
#     return str('Flata por implementar')

# -----------------Cursos-------------------------


# def crear_curso(json):
#     return str(db.cursos.insert_one(json).inserted_id)


def consultar_post_por_id(id_post):
    container = db.get_container_client("Publications")
    items = list(container.query_items(
        query="SELECT * FROM p WHERE p.identifier=@identifier",
        parameters=[
            { "name":"@identifier", "value": id_post }
        ]
    ))

    return items

def consultar_comment_por_post(id_publication):
    container = db.get_container_client("Comments")
    items = list(container.query_items(
        query="SELECT * FROM c WHERE c.id_publication=@id_publication",
        parameters=[
            { "name":"@id_publication", "value": id_publication }
        ]
    ))

    return items
    # return list(db.Comments.find({'id_publication': id_post},{"_id":0}))


# def actualizar_curso(curso):
#     # Esta funcion solamente actualiza nombre, descripcion y clases del curso
#     return str(db.cursos.update_one({'_id': ObjectId(curso['_id'])},  {'$set': {'nombre': curso['nombre'],'descripcion': curso['descripcion'],'clases': curso['clases']}}).modified_count)


# def borrar_curso_por_id(curso_id):
#     return str(db.cursos.delete_one({'_id': ObjectId(curso_id)}).deleted_count)


# def consultar_curso_por_id_proyeccion(id_curso, proyeccion=None):
#     return str('Flata por implementar')