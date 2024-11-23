import json
import random

from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity

from log import Logger

from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from waitress import serve
from pcrf.pcrf import Pcrf
from auth import Authenticate
import const

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config["JWT_SECRET_KEY"] = const.JWT_SECRET_KEY
jwt = JWTManager(app)
api = Api(app)

logger = Logger.getLogger('server_requests', 'logs/server_requests')


def random_ref(length):
    sample_string = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'  # define the specific string
    # define the condition for random string
    return ''.join((random.choice(sample_string)) for x in range(length))


@jwt.expired_token_loader
def my_expired_token_callback(jwt_header, jwt_data):
    return jsonify({"result": "error", "msg": "Token has expired"}), 401


@jwt.invalid_token_loader
def my_invalid_token_callback(jwt_data):
    return jsonify({"result": "error", "msg": "Invalid Token"}), 401


@jwt.unauthorized_loader
def my_unauthorized_loader_callback(jwt_data):
    return jsonify({"result": "error", "msg": "Missing Authorization Header"}), 401


def getAuthKey(userid):
    with open('auth.json') as f:
        data = json.load(f)
        for usr in data['user_list']:
            if usr['username'] == str(userid):
                return usr['authkey']


# TOKEN
class GetToken(Resource):
    def get(self):
        logger.info(ref + " - " + str(request.remote_addr) + " - " + str(request.url) + " - " + str(request.headers))
        data = request.get_json()
        return Authenticate.generateToken(data, ref)


# PCRF
# class PcrfProvision(Resource):
#     @jwt_required()
#     def post(self):
#         logger.info(ref + " - " + str(request.remote_addr) + " - " + str(request.url) + " - " + str(request.headers))
#         data = request.get_json()
#         getauth = getAuthKey(data['userID'])
#
#         authkey = get_jwt_identity()
#         if authkey == getauth:
#
#             if data['type'] == 'ADDON_CREATE':
#                 return Pcrf.pcrfAddonCreate(data,ref)
#             if data['type'] == 'ADDON_DELETE':
#                 return Pcrf.pcrfAddonDelete(data,ref)
#         else:
#             return {"msg": "UnAuthorized"}

class Recharge(Resource):
    #@jwt_required()
    def post(self):
        ref = random_ref(15)
        logger.info(ref + " - " + str(request.remote_addr) + " - " + str(request.url) + " - " + str(request.headers))
        data = request.get_json()

        try:
            if data['workOrderType'] and data['orderObjectType'] and data['orderObjectKey'] and data['cardSequence'] and \
                    data['rechargeAmount'] and data['balanceBeforeRecharge'] and data['balanceAfterRecharge'] and data['expiryDate']:
                return {'result': 'success', 'description': 'SLT_PCRF is not provisioned yet.', 'data': data}
            else:
                return {'result': 'error', 'description': 'request json value parameter data missing', 'data': data}
        except Exception as e:
            return {'result': 'error', 'description': 'request json key parameter wrong or missing', 'data': data}


class Offeractivate(Resource):
    #@jwt_required()
    def post(self):
        ref = random_ref(15)
        logger.info(ref + " - " + str(request.remote_addr) + " - " + str(request.url) + " - " + str(request.headers))
        data = request.get_json()
        logger.info(ref + " - " + str(data))
        try:
            if data['workOrderType'] and data['orderObjectType'] and data['orderObjectKey'] and data['offeringID'] and \
                    data['purchaseSeq'] and data['effectiveTime'] and data['expirationTime'] and data['activationTime']:
                #return {'result': 'success', 'description': 'SLT_PCRF is not provisioned yet.', 'data': data}
                return Pcrf.pcrfAddonCreate(data, ref)
            else:
                return {'result': 'error', 'description': 'request json value parameter data missing', 'data': data}
        except Exception as e:
            return {'result': 'error', 'description': 'request json key parameter wrong or missing', 'data': data}


class ChangeOfferStatus(Resource):
    #@jwt_required()
    def post(self):
        ref = random_ref(15)
        logger.info(ref + " - " + str(request.remote_addr) + " - " + str(request.url) + " - " + str(request.headers))
        data = request.get_json()
        try:
            if data['workOrderType'] and data['orderObjectType'] and data['orderObjectKey'] and data['offeringID'] and \
                    data['purchaseSeq'] and data['statusTime']:
                return {'result': 'success', 'description': 'SLT_PCRF is not provisioned yet.', 'data': data}
            else:
                return {'result': 'error', 'description': 'request json value parameter data missing', 'data': data}
        except Exception as e:
            return {'result': 'error', 'description': 'request json key parameter wrong or missing', 'data': data}


class ChangeSubStatus(Resource):
    #@jwt_required()
    def post(self):
        ref = random_ref(15)
        logger.info(ref + " - " + str(request.remote_addr) + " - " + str(request.url) + " - " + str(request.headers))
        data = request.get_json()
        try:
            if data['workOrderType'] and data['orderObjectType'] and data['orderObjectKey'] and data['oldStatus'] and \
                    data['newStatus'] and data['statusTime']:
                return {'result': 'success', 'description': 'SLT_PCRF is not provisioned yet.', 'data': data}
            else:
                return {'result': 'error', 'description': 'request json value parameter data missing', 'data': data}
        except Exception as e:
            return {'result': 'error', 'description': 'request json key parameter wrong or missing', 'data': data}


class BalanceExhaust(Resource):
    #@jwt_required()
    def post(self):
        ref = random_ref(15)
        logger.info(ref + " - " + str(request.remote_addr) + " - " + str(request.url) + " - " + str(request.headers))
        data = request.get_json()
        try:
            if data['workOrderType'] and data['orderObjectType'] and data['orderObjectKey'] and data[
                'primaryIdentity'] and data['accountType'] and data['accountInstanceId'] and data['effectiveTime'] and \
                    data['expireTime'] and data['totalAmount']:
                return {'result': 'success', 'description': 'SLT_PCRF is not provisioned yet.', 'data': data}
            else:
                return {'result': 'error', 'description': 'request json value parameter data missing', 'data': data}
        except Exception as e:
            return {'result': 'error', 'description': 'request json key parameter wrong or missing', 'data': data}


# API URL PATH
# TOKEN
api.add_resource(GetToken, const.APP_ROUTE_TOKEN)

# PCRF
# api.add_resource(PcrfProvision, const.APP_ROUTE_PCRF)

api.add_resource(Recharge, const.APP_ROUTE_RECHARGE)
api.add_resource(Offeractivate, const.APP_ROUTE_OFFERACTIVATE)
api.add_resource(ChangeOfferStatus, const.APP_ROUTE_CHANGEOFFERSTAT)
api.add_resource(ChangeSubStatus, const.APP_ROUTE_CHANGESTAT)
api.add_resource(BalanceExhaust, const.APP_ROUTE_BALANCEEXHAUST)

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=20001, threads=3)
