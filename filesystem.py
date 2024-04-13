import os
import json

DATA_PATH = f'./static/data'
IMAGE_PATH = f'./static/image'
DEFAULT_LANG = 'en'

class Filesystem:
    
    def getEndpoints(self):
        return [f for f in os.listdir(self.__dataDirectory()) if os.path.isdir(self.__dataDirectory(f))]
    
    def getEndpointEntities(self, endpoint):
        is_endpoint = os.path.isdir(self.__dataDirectory(endpoint))
        
        # 404, not found
        if not is_endpoint:
            return {'error' : f'Endpoint {endpoint} not found. Go to /endpoints to see a list of available endpoints'}, 404
             
        return [f for f in os.listdir(self.__dataDirectory(endpoint)) if os.path.isdir(self.__dataDirectory(endpoint, f))]

    def getEntity(self, endpoint: str, entity: str, lang:str = DEFAULT_LANG):
        entityPath = os.path.join(self.__dataDirectory(endpoint, entity), f'{lang}.json' )
        exists = os.path.isfile(entityPath)

        if not exists:
            return {'error' : f'Entity /{endpoint}/{entity} not found.'}, 404
        
        with open(entityPath) as user_file:
            parsed_json = json.load(user_file)

        return parsed_json


    def __dataDirectory(self, endpoint: str = '', entity: str = '') -> str:
        return os.path.join(DATA_PATH.lower(), endpoint.lower(), entity.lower())
    
    def __imageDirectory(self, endpoint: str = '') -> str:
        return os.path.join(IMAGE_PATH, endpoint)