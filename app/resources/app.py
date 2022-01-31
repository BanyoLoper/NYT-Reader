from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from .model import Token
import requests
import os

app = Flask(__name__)

# Vamos a Explorar un poco con las APIs del New York Reader
# API Base: 
# Specified API: /lists/best-sellers/history.json 
# API Key: ELktWPwCBRM2iM6J5Tjdxj5oQH4bLcBn

SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgersql://postgres:frigon@localhost/nyt_reader'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'secret string'

api_base = 'https://api.nytimes.com/svc/books/v3'
api_specific = '/lists/best-sellers/history.json' 
query = '?api-key=ELktWPwCBRM2iM6J5Tjdxj5oQH4bLcBn'

@app.route('/')
def hello_world():
    url = api_base + api_specific + query
    request = requests.get(url)
    data = request.json()
    results = data['results']
    titles = {}
    print(type(results))
    for i,title in enumerate(data['results']):
        titles['title' + str(i)] = title['title']
    entry = Token("nyt_books",'test')
    db.session.add(entry)
    db.session.commit()
    
    return jsonify(data)
