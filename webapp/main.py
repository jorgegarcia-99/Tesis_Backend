from __future__ import unicode_literals

from flask import Flask, request, current_app, Response, render_template, session, redirect, url_for
from flask_cors import CORS
from pymongo import MongoClient, DESCENDING
from werkzeug.local import LocalProxy
from . import error_handlers

import json
import requests
import pandas as pd


app = Flask(__name__)
CORS(app)


client = MongoClient('mongodb+srv://admin:UMPePqM6AK7odzGB@scrapyfacebook.qgn65.mongodb.net/test?authSource=admin&replicaSet=atlas-c4innp-shard-0&readPreference=primary&appname=MongoDB%20Compass&ssl=true')

@app.route('/scrape/comments', methods = ['POST'])
def scrapeComment():

    request_data = request.get_json()
    spider_name = request_data['spider_name']
    url = request_data['url']

    params = {
        'spider_name': spider_name,
        'url': url,
    }
    
    response = requests.get('http://localhost:9080/crawl.json', params)
    data = json.loads(response.text)
    return data

@app.route('/scrape/post', methods = ['POST'])
def scrapePost():

    request_data = request.get_json()
    url = request_data['url']

    if 'facebook' in url:
        spider_name = 'spider_post'
    
        params = {
            'spider_name': spider_name,
            'crawl_args': json.dumps({'url': url}),
            'start_requests': True
        }

        response = requests.get('http://localhost:9080/crawl.json', params)
        data = json.loads(response.text)
        
        if data["items"][0]["identifier"]:
            result = client['DBRedSocial']['Comments'].find(filter={'id_publication':data["items"][0]["identifier"]})
            print(json.dumps(result))

            return data