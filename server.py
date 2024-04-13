from flask import Flask, request
from flask_cors import CORS
import os
from filesystem import Filesystem

app = Flask(__name__)
CORS(app)

fsy = Filesystem()

@app.route('/')
@app.route('/endpoints')
def entry_point():
    return fsy.getEndpoints()

@app.route('/<endpoint>')
def endpoints(endpoint):
    return fsy.getEndpointEntities(endpoint)

@app.route('/<endpoint>/<entity>')
def entity(endpoint, entity):
    return fsy.getEntity(endpoint, entity)

if __name__ == '__main__':
    app.run(debug=True, port=8001)
