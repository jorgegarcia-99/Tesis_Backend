from flask import Blueprint, request, jsonify
from . import db
import requests
import json


bp = Blueprint('demo', __name__, url_prefix='/demo')

@bp.route('', methods=['GET', 'POST', 'PUT', 'DELETE'])
def demo():
   
    request_body = request.get_json()
    url = request_body['texto']
    
    if request.method == 'POST':
        response = requests.post('https://api-proyecto-nlp.herokuapp.com/predict', json = {"texto":url})
        return response.json()