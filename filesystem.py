import os
import json
from flask import send_file


DATA_PATH = f'./static/data'
IMAGE_PATH = f'./static/images'
DEFAULT_LANG = 'en'




class Filesystem:

    def getEndpoints(self):
        endpoints = [f for f in os.listdir(self.__dataDirectory()) if os.path.isdir(self.__dataDirectory(f))]
        return endpoints

    def getEndpointEntities(self, endpoint):
        is_endpoint = os.path.isdir(self.__dataDirectory(endpoint))

        # 404, not found
        if not is_endpoint:
            return {'error': f'Endpoint {endpoint} not found. Go to /endpoints to see a list of available endpoints'}, 404

        return [f for f in os.listdir(self.__dataDirectory(endpoint)) if os.path.isdir(self.__dataDirectory(endpoint, f))]

    def getEntity(self, endpoint: str, entity: str, lang: str = DEFAULT_LANG):
        entityPath = os.path.join(self.__dataDirectory(
            endpoint, entity), f'{lang}.json')
        exists = os.path.isfile(entityPath)

        if not exists:
            return {'error': f'Entity /{endpoint}/{entity} not found.'}, 404

        try:
            with open(entityPath) as user_file:
                parsed_json = json.load(user_file)
        except:
            return {'error': f'Error in JSON formatting of entity {endpoint}/${entity} for language {lang}'}, 500

        return parsed_json

    def getImages(self, endpoint: str, entity: str):
        is_endpoint = os.path.isdir(self.__dataDirectory(endpoint))
        is_entity = os.path.isdir(self.__dataDirectory(endpoint, entity))

        # 404, not found
        if not is_endpoint:
            return {'error': f'Endpoint {endpoint} not found. Go to /endpoints to see a list of available endpoints'}, 404

        # 404, not found
        if not is_entity:
            return {'error': f'Entity {entity} not found. Go to /{endpoint} to see a list of available entities'}, 404

        return [f for f in os.listdir(self.__imageDirectory(endpoint, entity)) if os.path.isfile(self.__imageDirectory(endpoint, entity, f), )]

    def getImage(self, endpoint: str, entity: str, image: str, format: str = 'webp'):
        imagePath = self.__imageDirectory(endpoint, entity, image)

        is_image = os.path.isfile(imagePath)
        if not is_image:
            return {'error': f'Image {entity}/{image} not found. Go to /{entity}/images to see a list of available images'}, 404

        return send_file(imagePath, mimetype=f'image/{format}'), 200

    def __dataDirectory(self, endpoint: str = '', entity: str = '') -> str:
        return os.path.join(DATA_PATH.lower(), endpoint.lower(), entity.lower())

    def __imageDirectory(self, endpoint: str = '', entity: str = '', image: str = '') -> str:
        return os.path.join(IMAGE_PATH.lower(), endpoint.lower(), entity.lower(), image.lower())
