import json
import random

from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity

from log import Logger

from flask import Flask, request, jsonify
from flask_restful import Api, Resource
#from waitress import serve
from pcrf.pcrf import Pcrf
#from auth import Authenticate
from requests.auth import HTTPBasicAuth
import const
import db

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
                logger.info(ref + " - " + str(data))
                return {'result': 'success', 'description': 'SLT_PCRF is not provisioned yet.', 'data': data}
            else:
                logger.info(ref + " - " + str(data))
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
        logger.info(ref + " - " + str(data))
        try:
            if data['workOrderType'] and data['orderObjectType']:
                return Pcrf.pcrfAddonDelete(data, ref)
            else:
                return {'result': 'error', 'description': 'request json value parameter data missing', 'data': data}
        except Exception as e:
            return {'result': 'error', 'description': 'request json key parameter wrong or missing', 'data': data}

#=======================
class callMySlt:
    def exeDb(self):
        try:
            conn = db.DbConnection.dbconnHadwh("")
            print(conn)
            if conn['status'] == "error":
                return conn
            else:  
                if self == "Primary Offering" or self == "Main Packages" or self == "Add-ons":
                    sql = 'SELECT * FROM OSS_FAULTS.LTE_OCS_PCRF_DATA WHERE PACKAGE_TYPE = :value'
                    c = conn['status'].cursor()
                    c.execute(sql,{'value':self})
                    result = {}
                    data=[]
                    for row in c:
                        data.append({"PACKAGE_TYPE": row[0],
                                    "ADDON_NAME": row[1],
                                    "MYSLT_PKG_NAME": row[2],
                                    "RECURRENCE": row[3],
                                    "DATA_VOLUME_GB": row[4],
                                    "VALIDITY": row[5],
                                    "PRICE_LKR_WITHOUT_TAX": row[6],
                                    "PRICE_LKR_WITH_TAX": row[7],
                                    "PACKAGE_ID": row[8],
                                    "PCRF_PKG_NAME": row[9],
                                    "OFFERING_NAME": row[10],
                                    "OFFERING_ID": row[11],
                                    "OFFERING_CATEGORY": row[12],
                                    "DATA_ACCOUNT_TYPE": row[13],
                                    "DATA_FREE_UNIT_TYPE": row[14],
                                    "VOICE_ACCOUNT_TYPE": row[15],
                                    "VOICE_FREE_UNIT_TYPE": row[16],
                                    "VOICE_VOLUME": row[17]})    
                    result['data'] = data
                    return result
                else:
                    sql = 'SELECT * FROM OSS_FAULTS.LTE_OCS_PCRF_DATA'
                    c = conn['status'].cursor()
                    c.execute(sql)
                    result = {}
                    data=[]
                    for row in c:
                        data.append({"PACKAGE_TYPE": row[0],
                                    "ADDON_NAME": row[1],
                                    "MYSLT_PKG_NAME": row[2],
                                    "RECURRENCE": row[3],
                                    "DATA_VOLUME_GB": row[4],
                                    "VALIDITY": row[5],
                                    "PRICE_LKR_WITHOUT_TAX": row[6],
                                    "PRICE_LKR_WITH_TAX": row[7],
                                    "PACKAGE_ID": row[8],
                                    "PCRF_PKG_NAME": row[9],
                                    "OFFERING_NAME": row[10],
                                    "OFFERING_ID": row[11],
                                    "OFFERING_CATEGORY": row[12],
                                    "DATA_ACCOUNT_TYPE": row[13],
                                    "DATA_FREE_UNIT_TYPE": row[14],
                                    "VOICE_ACCOUNT_TYPE": row[15],
                                    "VOICE_FREE_UNIT_TYPE": row[16],
                                    "VOICE_VOLUME": row[17]}) 
                    result['data'] = data
                    return result
        except Exception as e:
            #result['data']= {"status": "error","errors": "DB Connection Error"}
            #logger.info("Exception : %s" % ref + " - " + str(e))
            return str(e)

class getDetails(Resource):
    def post(self):         
        data = request.get_json()
        return  callMySlt.exeDb(data['packageType'])

#==================================================
loggerocsApi = Logger.getLogger('OCSOffer', 'logs/OCSOffer') 
loggeroffer = Logger.getLogger('add_del_Offer', 'logs/add_del_Offer')

headers = {
    'Content-type': 'application/json',
    'Accept': 'application/json'}
    #'Authorization': f'Basic 'SLTUSR':'SLTPW''} 
auth = HTTPBasicAuth('SLTUSR', 'SLTPW')  

class offerRecharge(Resource):
  
    def post(self):         
        data = request.get_json()     
        loggerocsApi.info("data : %s" % data)
        try:
            if data ['msisdnNo'] and data ['productId'] and data ['offerName'] and data ['operationType'] and data ['channelName']:
                
                if data ['operationType'] == 'ADD_OFFERING':                    
                    retmsg = OCSaddOffer.OCS_ADD_Offer (data ['msisdnNo'],data ['productId'],data ['operationType'])    
                    loggerocsApi.info("retmsgadd : %s" % retmsg)                       
                  
                elif data ['operationType'] == 'DEL_OFFERING':
                    retmsg = OCSaddOffer.OCS_ADD_Offer (data ['msisdnNo'],data ['productId'],data ['operationType'])
                    loggerocsApi.info("retmsgdel : %s" % retmsg) 
                    
                print(retmsg['resultHeader']['resultCode'])
                loggerocsApi.info("result1 : %s" % retmsg)
                    
                if (retmsg['resultHeader']['resultCode'])== '0':
                    return {'result': 'success','data': retmsg} 
                else:
                    return {'result': 'error','data': retmsg} 
            else:            
                return {'result': 'error', 'description': 'request json value parameter data missing','data': data} 
                #return {'result': retmsg}         
        except Exception as e:
            return {'result': 'error', 'description': 'request json key parameter wrong or missing','data': data} 

class OCSaddOffer:
    
    def OCS_ADD_Offer(self, OfferId ,OfferType):
        
        data = {
                "requestHeader": {
                "operationType": OfferType,
                "requestedBy": "slt",
                "systemName": "SLT_OCS_INT"
                },
                "primaryIdentity": self,
                "offeringList": [
                {
                "offeringId": OfferId,
                "purchaseSeq": "null"
                }
                ]
                }

        loggeroffer.info("Request : %s" % data)
        try:

            response = requests.post('http://10.253.0.158/sltServices/ocs/integration/offering', data=json.dumps(data),
                                           headers=headers,auth=auth)

            loggeroffer.info("Response Code: %s" % response.status_code)
            resmsg = response.json()
            #responsedata = {"data": resmsg['data']}
            loggeroffer.info("Response : %s" % resmsg)

            return resmsg
        except Exception as e:
            print("Exception : %s" % traceback.format_exc())
            loggeroffer.info("Exception : %s" % traceback.format_exc())

class getmobileDetails(Resource):
    #@jwt_required()
    def post(self):         
        data = request.get_json()
	#loggerocsApi.info("data : %s" % data)
        return  getNumber.clarityDb(data['msisdnNo'])
        

class getNumber:
    def clarityDb(self):
        try:
            conn = db.DbConnection.dbconnClarity("")
            print(conn)     
            if conn['status'] == "error":
                return conn
            else:  
                if self is not None:
                    parmList = [self,'INSERVICE','SUSPENDED','CUSTOMER CONTACT NO','CUSTOMER CONTACT']
                    sql = 'SELECT C.CIRT_DISPLAYNAME,C.CIRT_SERT_ABBREVIATION,C.CIRT_STATUS ,SA.SATT_ATTRIBUTE_NAME,SA.SATT_DEFAULTVALUE FROM CIRCUITS C, SERVICES_ATTRIBUTES SA WHERE CIRT_DISPLAYNAME = :1 AND CIRT_SERV_ID = SATT_SERV_ID and CIRT_STATUS in (:2,:3) AND SATT_ATTRIBUTE_NAME IN (:4,:5)'                    
                    c = conn['status'].cursor()
                    #c.execute(sql,{'value':self})
                    c.execute(sql,parmList)
                    results = c.fetchall()
                    print("results:", results)
                    # Get the row count
                    row_count = len(results)
                    result = {}
                    data=[]
                    if row_count == 0:
                        result['data'] = 'No data found'
                        logger.info("DB Output " + str(result['data'])) 
                        return result
                    else:
                        for row in results:
                            data.append({"CIRT_DISPLAYNAME": row[0],
                                         "CIRT_SERT_ABBREVIATION": row[1],
                                         "CIRT_STATUS": row[2],
                                         "SATT_ATTRIBUTE_NAME": row[3],
                                         "SATT_DEFAULTVALUE": row[4]})   
                        result['data'] = data
                        print(data[0])
                        logger.info("DB Output " + str(data[0])) 
                        return result
        except Exception as e:
            result['data']= {"status": "error","errors": "DB Connection Error " + str(e)}
            #logger.info("Exception : %s" % ref + " - " + str(e))
            logger.info("Exception " + str(e) )
            return result['data']  

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
api.add_resource(getmobileDetails, const.APP_ROUTE_GETMOBILE)

# Modify Routes
api.add_resource(getDetails, const.APP_ROUTE_MAPPING)

#offer
api.add_resource(offerRecharge, const.APP_ROUTE_OFFER)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=20001)
