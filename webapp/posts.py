from flask import Blueprint, request, jsonify, abort
from . import db
from webapp.model import model
from webapp.preprocesamiento import preprocesamiento
import requests
import json
import pandas as pd

bp = Blueprint('posts', __name__, url_prefix='/scrape')

def response_scrapy(spider_name,url):

    params = {
        'spider_name': spider_name,
        'crawl_args': json.dumps({'url': url}),
        'start_requests': True
    }
 
    response_post = requests.get('https://tp2-scrapyrt.azurewebsites.net/crawl.json', params)
    data = json.loads(response_post.text)

    if spider_name == 'spider_post':
        if len(data["items"]) == 0:
            abort(404)
        else:
            if (data["items"][0]['identifier'] == None):
                abort(404)

    return data

def sentiment_analysis(text):   
    return model(preprocesamiento(text))
        
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
                result = db.consultar_comment_por_post(dict_post["identifier"])
                  
                if result:
                    dict_post.update({'comments': list(result)})            

                else:
                    data_comment = response_scrapy('spider_comment', url)
                    list_dict_comment = list(data_comment["items"])
                    dict_post.update({'comments': list_dict_comment})  
                
                if len(dict_post["comments"])==0:
                    dict_post.update({'comments_positive': num_positivo})
                    dict_post.update({'comments_negative': num_negativo})
                    dict_post.update({'comments_neutral': num_neutro})
                    dict_post.update({'comments': []})
                    return dict_post

                
                df_comments = pd.DataFrame(dict_post["comments"])
                
                if 'sentiment' not in df_comments.columns:
                    df_comments["sentiment"] = df_comments["text"].transform(sentiment_analysis)
                
                frec = df_comments["sentiment"].value_counts()

                if "Positivo" in list(frec.keys()): num_positivo = int(frec.loc[["Positivo"]][0])
                if "Negativo" in list(frec.keys()): num_negativo = int(frec.loc[["Negativo"]][0])
                if "Neutro" in list(frec.keys()): num_neutro = int(frec.loc[["Neutro"]][0])

                dict_post.update({'comments_positive': num_positivo})
                dict_post.update({'comments_negative': num_negativo})
                dict_post.update({'comments_neutral': num_neutro})

                dict_post.update({'comments': list(df_comments.T.to_dict().values())})

                return dict_post
        
        else:
            abort(404)
    
    elif request.method == 'PUT':
        pass
    elif request.method == 'DELETE' and url is not None:
        pass
    
    return 'OK'
