from flask import Blueprint, request, jsonify
from . import db
from webapp.model import svm_model
from webapp.preprocesamiento import preprocesamiento


bp = Blueprint('demo', __name__, url_prefix='/demo')

@bp.route('', methods=['GET', 'POST', 'PUT', 'DELETE'])
def demo():
   
    request_body = request.get_json()
    texto = request_body['texto']
    
    if request.method == 'POST':
        preprocesado = preprocesamiento(texto)
        resultado = svm_model(preprocesado)
        return jsonify({"texto":texto,"preprocesado":preprocesado,"resultado":resultado})