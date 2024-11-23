from flask import jsonify
from flask_jwt_extended import create_access_token

from log import Logger

logger = Logger.getLogger('token', 'logs/token')


class Authenticate:

    def generateToken(self, ref):
        access_token = create_access_token(identity=self['api_key'])
        logger.info("Token : %s" % ref + " - " + str(access_token))
        return jsonify(access_token=access_token)
