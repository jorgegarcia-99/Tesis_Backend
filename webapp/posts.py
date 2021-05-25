from flask import Blueprint, request, jsonify, abort
from . import db
import requests
import json


bp = Blueprint('posts', __name__, url_prefix='/scrape')

def response_scrapy(spider_name,url):

    params = {
        'spider_name': spider_name,
        'crawl_args': json.dumps({'url': url}),
        'start_requests': True
    }
 
    response_post = requests.get('http://40.71.230.0:9080/crawl.json', params)
    data = json.loads(response_post.text)

    if spider_name == 'spider_post':
        if len(data["items"]) == 0:
            abort(404)
        else:
            if (data["items"][0]['identifier'] == None):
                abort(404)

    return data
        
@bp.route('', methods=['GET', 'POST', 'PUT', 'DELETE'])
def extract():
   
    request_body = request.get_json()
    url = request_body['url']

    if request.method == 'POST':
        if 'facebook' in url or 'fb' in url:

            data_post = response_scrapy('spider_post', url)

            dict_post = dict(data_post["items"][0])
            num_negativo = 0
            num_positivo = 0
            num_neutro = 0

            if dict_post["identifier"]:
                result = db.consultar_post_por_id(dict_post["identifier"])

                if result:
                    dict_post.update({'comments': list(result)})              

                else:
                    data_comment = response_scrapy('spider_comment', url)
                    list_dict_comment = list(data_comment["items"])
                    dict_post.update({'comments': list_dict_comment})  

                for comment in dict_post["comments"]:
                    response = requests.post('https://api-proyecto-nlp.herokuapp.com/predict', json = {"texto":comment["text"]})
                    comment["sentiment"] = response.json()["resultado"]

                    if response.json()["resultado"] == "Positivo": num_positivo += 1
                    elif response.json()["resultado"] == "Negativo": num_negativo += 1
                    elif response.json()["resultado"] == "Neutro": num_neutro += 1

                dict_post.update({'comments_positive': num_positivo})
                dict_post.update({'comments_negative': num_negativo})
                dict_post.update({'comments_neutral': num_neutro})

                return dict_post
        
        else:
            abort(404)
    
    elif request.method == 'PUT':
        pass
    elif request.method == 'DELETE' and url is not None:
        pass
    
    return 'OK'
