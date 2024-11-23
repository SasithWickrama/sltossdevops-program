import random

from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from mail.sendmail import SendMail
import const
from log import Logger

logger = Logger.getLogger('server_requests', 'logs/server_requests')

app = Flask(__name__)
api = Api(app)

def random_ref(length):
    sample_string = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'  # define the specific string
    # define the condition for random string
    return ''.join((random.choice(sample_string)) for x in range(length))




class Entmail(Resource):
    def post(self):
        ref = random_ref(15)
        data = request.get_json()
        logger.info(ref + " - " + str(request.remote_addr) + " - " + str(request.url) + " - " + str(request.headers)+ " - " + str(data))
        return  SendMail.sendMail(data,ref)



api.add_resource(Entmail, const.APP_ROUTE_ENTMAIL)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=22555)