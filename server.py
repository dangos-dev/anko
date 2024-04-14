from flask import Flask, request
from flask_caching import Cache
from filesystem import Filesystem

config = {
    "DEBUG": True,
    "CACHE_TYPE": "SimpleCache",
    "CACHE_DEFAULT_TIMEOUT": 300
}

cache = Cache(config=config)

app = Flask(__name__)
app.config.from_mapping(config)
cache = Cache(app)

fsy = Filesystem()


@app.route('/')
@app.route('/endpoints')
@cache.cached()
def entry_point():
    return fsy.getEndpoints()


@app.route('/<endpoint>')
@cache.cached()
def endpoints(endpoint):
    return fsy.getEndpointEntities(endpoint)


@app.route('/<endpoint>/all')
@cache.cached()
def entities_all(endpoint):
    availableEntities = fsy.getEndpointEntities(endpoint)
    entities = []
    for entity in availableEntities:
        entities.append(fsy.getEntity(endpoint, entity))

    return entities


@app.route('/<endpoint>/<entity>')
@cache.cached()
def entity(endpoint, entity):
    return fsy.getEntity(endpoint, entity)


@app.route('/<endpoint>/<entity>/images')
@cache.cached()
def images(endpoint, entity):
    return fsy.getImages(endpoint, entity)


@app.route('/<endpoint>/<entity>/<image>')
@app.route('/<endpoint>/<entity>/<image>/<format>')
def image(endpoint, entity, image, format='webp'):
    return fsy.getImage(endpoint, entity, image, format)


if __name__ == '__main__':
    app.run(debug=True, port=8001)
