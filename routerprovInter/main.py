import json
import random
import requests
from log import Logger
from flask import Flask, request, jsonify
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

logger_server = Logger.getLogger('server_requests', 'logs/server_requests')
logger_router = Logger.getLogger('router_requests', 'logs/router_requests')

def random_ref(length):
    sample_string = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'  # define the specific string
    # define the condition for random string
    return ''.join((random.choice(sample_string)) for x in range(length))


class requestMapping(Resource):
    #@jwt_required()
    def post(self):
        ref = random_ref(15)
        logger_server.info(ref + " - " + str(request.remote_addr) + " - " + str(request.url) + " - " + str(request.headers))
        data = request.get_json()

        try:
            
            logger.info("Request : %s" % ref + " - " + str(data))
            return Pcrf.Recharge(data, ref)
            logger.info("Response : %s" % ref + " - " + str(result))

        except Exception as e:
            return {'result': 'error', 'description': 'request json key parameter wrong or missing', 'data': data}


# requestMapping Routes
api.add_resource(requestMapping, '/api/RouterConfig/modifyspeed')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7005)
