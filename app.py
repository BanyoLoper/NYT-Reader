from flask import Flask, jsonify
import requests

app = Flask(__name__)

# Vamos a Explorar un poco con las APIs del New York Reader
# API Base: 
# Specified API: /lists/best-sellers/history.json 
# API Key: ELktWPwCBRM2iM6J5Tjdxj5oQH4bLcBn

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
    print("test ")
    return jsonify(data)
