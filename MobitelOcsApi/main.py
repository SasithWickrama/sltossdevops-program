import json
import random
import requests
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
from sms import Sendsms

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
            return Pcrf.Recharge(data, ref)
            # if data['workOrderType'] and data['orderObjectType'] :
            #     return Pcrf.Recharge(data, ref)
            # else:
            #     return {'result': 'error', 'description': 'request json value parameter data missing', 'data': data}
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
            if data['workOrderType'] and data['orderObjectType']:

                return Pcrf.chnageSubStatus(data, ref)

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

        ref = random_ref(15)
        data = request.get_json()
        loggerocsApi.info(ref + ": " + "data : %s" % data)

        try:

            if data ['msisdnNo'] and data ['productId'] and data ['offerName'] and data ['operationType'] and data ['channelName']:

                data ['channelSeq'] = None

                #Offer Add only OCS provisioning
                if data ['operationType'] == 'ADD_OFFERING' and (data['productId'] != '61000011' and data['productId'] != '61000012'):

                    retmsg = OCSaddOffer.OCS_ADD_Offer (data ['msisdnNo'],data ['productId'],data ['operationType'],data ['channelSeq'])
                    loggerocsApi.info(ref + ": " + "retmsgadd : %s" % retmsg)

                    if retmsg['resultHeader']['resultCode'] == '0':
                        return {'result': 'success','dataOcs': 'ADD_OFFERING: ' + retmsg['resultHeader']['resultDesc'],'dataPcrf' : 'Offer ID is not relevant to PCRF provisioning'}
                    else:
                        return {'result': 'error','dataOcs': 'ADD_OFFERING: ' + retmsg['resultHeader']['resultDesc'],'dataPcrf' : 'Offer ID is not relevant to PCRF provisioning'}

                #Offer Delete only OCS provisioning
                elif data ['operationType'] == 'DEL_OFFERING' and (data['productId'] != '61000011' and data['productId'] != '61000012'):

                    retmsg = OCSaddOffer.OCS_ADD_Offer (data ['msisdnNo'],data ['productId'],data ['operationType'],data ['channelSeq'])
                    loggerocsApi.info(ref + ": " + "retmsgadd : %s" % retmsg)

                    if retmsg['resultHeader']['resultCode'] == '0':
                        return {'result': 'success','dataOcs':  'DEL_OFFERING ' + retmsg['resultHeader']['resultDesc'],'dataPcrf' : 'Offer ID is not relevant to PCRF provisioning'}
                    else:
                        return {'result': 'error','dataOcs': 'DEL_OFFERING ' + retmsg['resultHeader']['resultDesc'],'dataPcrf' : 'Offer ID is not relevant to PCRF provisioning'}

                #Offer Add for both OCS and PCRF provisioning but not success
                elif data ['operationType'] == 'ADD_OFFERING' and (data['productId'] == '61000011' or data['productId'] == '61000012'):

                    retmsg = OCSaddOffer.OCS_ADD_Offer (data ['msisdnNo'],data ['productId'],data ['operationType'],data ['channelSeq'])
                    loggerocsApi.info(ref + ": " + "retmsgadd : %s" % retmsg)

                    if retmsg['resultHeader']['resultCode'] == '0':
                        retmsg_pcrf = Pcrf.pcrfAddonCreate(data, ref)
                        loggerocsApi.info(ref + ": " + "retmsg_pcrf : %s" % retmsg_pcrf)

                    else:
                        return {'result': 'error','dataOcs': 'ADD_OFFERING ' + retmsg['resultHeader']['resultDesc'],'dataPcrf' : 'PCRF platform is not provisioned due to '+ retmsg['resultHeader']['resultDesc']}

                    if retmsg['resultHeader']['resultCode'] == '0' and retmsg_pcrf['result'] == 'error':

                        if "changeSubOfferingResult" in retmsg:

                            puchseq = retmsg['changeSubOfferingResult']['offering']

                            if "purchasingSeq" in puchseq[0]['offeringKey']:
                                loggerocsApi.info(ref + ": " + "purchasingSeq : %s" % puchseq[0]['offeringKey']['purchasingSeq'])
                                retmsgDel = OCSaddOffer.OCS_ADD_Offer (data ['msisdnNo'],data ['productId'],'DEL_OFFERING',puchseq[0]['offeringKey']['purchasingSeq'])
                                loggerocsApi.info(ref + ": " + "retmsgDeloffer : %s" % retmsgDel)
                                if retmsgDel['resultHeader']['resultCode'] == '0':

                                    retTaxPrice = getPackageprice(data['productId'])

                                    if retTaxPrice is not None:
                                        loggerocsApi.info(ref + ": " + "retmsgTaxPrice : %s" % retTaxPrice)

                                        if retTaxPrice is not None:

                                            retmsgadjustment = OCSadjustment.OCS_adjustment (data ['msisdnNo'],(retTaxPrice),"2")
                                            loggerocsApi.info(ref + ": " + "retmsgAdjustment: %s" % retmsgadjustment)

                                            return {'result': 'error','dataOcs': 'ADJUSTMENT ' + retmsgadjustment['resultHeader']['resultDesc'],'dataPcrf' : 'PCRF error provisioned'}

                                        else:
                                            return {'result': 'error','dataOcs': 'TaxPrice null against productId','dataPcrf' : 'PCRF error provisioned'}
                                    else:
                                        return {'result': 'error','dataOcs': 'TaxPrice null against productId','dataPcrf' : 'PCRF error provisioned'}

                                else:
                                    return {'result': 'error','dataOcs': 'DEL_OFFERING: ' + retmsgDel['resultHeader']['resultDesc'],'dataPcrf' : 'PCRF error provisioned'}
                            else:
                                return {'result': 'error','dataOcs': retmsg['resultHeader']['resultDesc'],'dataPcrf' : retmsg_pcrf['description']}
                        else:
                            return {'result': 'error','dataOcs': retmsg['resultHeader']['resultDesc'],'dataPcrf' : retmsg_pcrf['description']}

                    #Offer Add for both OCS and PCRF Provisioning both Success
                    elif retmsg['resultHeader']['resultCode'] == '0' and retmsg_pcrf['result'] == 'success':
                        return {'result': 'success','dataOcs': retmsg['resultHeader']['resultDesc'],'dataPcrf' : retmsg_pcrf['description']}
                    else:
                        return {'result': 'error','dataOcs': retmsg['resultHeader']['resultDesc'],'dataPcrf' : retmsg_pcrf['description']}

                #Offer Add for both OCS and PCRF Provisioning both Success
                elif data ['operationType'] == 'DEL_OFFERING'and (data['productId'] == '61000011' or data['productId'] == '61000012'):

                    retmsg = OCSaddOffer.OCS_ADD_Offer (data ['msisdnNo'],data ['productId'],data ['operationType'],data ['channelSeq'])
                    loggerocsApi.info(ref + ": " + "retmsgadd : %s" % retmsg)

                    if retmsg['resultHeader']['resultCode'] == '0':
                        retmsg_pcrf = Pcrf.pcrfAddonCreate(data, ref)
                        loggerocsApi.info(ref + ": " + "retmsg_pcrf : %s" % retmsg_pcrf)

                    else:
                        return {'result': 'error','dataOcs': 'DEL_OFFERING ' + retmsg['resultHeader']['resultDesc'],'dataPcrf' : 'PCRF platform is not provisioned due to '+ retmsg['resultHeader']['resultDesc']}

                    if retmsg['resultHeader']['resultCode'] == '0' and retmsg_pcrf['result'] == 'error':

                        if "changeSubOfferingResult" in retmsg:

                            puchseq = retmsg['changeSubOfferingResult']['offering']

                            if "purchasingSeq" in puchseq[0]['offeringKey']:

                                retmsgDel = OCSaddOffer.OCS_ADD_Offer (data ['msisdnNo'],data ['productId'],'ADD_OFFERING',puchseq[0]['offeringKey']['purchasingSeq'])
                                loggerocsApi.info(ref + ": " + "retmsgDeloffer : %s" % retmsgDel)
                                if retmsgDel['resultHeader']['resultCode'] == '0':

                                    retTaxPrice = getPackageprice(data['productId'])

                                    if retTaxPrice is not None:
                                        loggerocsApi.info(ref + ": " + "retmsgTaxPrice : %s" % retTaxPrice)

                                        if retTaxPrice is not None:

                                            retmsgadjustment = OCSadjustment.OCS_adjustment (data ['msisdnNo'],(retTaxPrice),"1")
                                            loggerocsApi.info(ref + ": " + "retmsgAdjustment: %s" % retmsgadjustment)

                                            return {'result': 'error','dataOcs': 'ADJUSTMENT ' + retmsgadjustment['resultHeader']['resultDesc'],'dataPcrf' : 'PCRF error provisioned'}

                                        else:
                                            return {'result': 'error','dataOcs': 'TaxPrice null against productId','dataPcrf' : 'PCRF error provisioned'}
                                    else:
                                        return {'result': 'error','dataOcs': 'TaxPrice null against productId','dataPcrf' : 'PCRF error provisioned'}

                                else:
                                    return {'result': 'error','dataOcs': 'ADD_OFFERING: ' + retmsgDel['resultHeader']['resultDesc'],'dataPcrf' : 'PCRF error provisioned'}
                            else:
                                return {'result': 'error','dataOcs': retmsg['resultHeader']['resultDesc'],'dataPcrf' : retmsg_pcrf['description']}
                        else:
                            return {'result': 'error','dataOcs': retmsg['resultHeader']['resultDesc'],'dataPcrf' : retmsg_pcrf['description']}
                else:
                    return {'result': 'error','dataOcs': retmsg['resultHeader']['resultDesc'],'dataPcrf' : retmsg_pcrf['description']}
            else:
                return {'result': 'error', 'description': 'request json value parameter data missing','data': 'PCRF error'}
                #return {'result': retmsg}
        except Exception as e:
            print(e)
            return {'result': 'error', 'description': 'request json key parameter wrong or missing','data': e}



class OCSaddOffer:

    def OCS_ADD_Offer(self, OfferId ,OfferType ,channelSeq):

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
                    "purchaseSeq": channelSeq
                }
            ]
        }

        loggeroffer.info("Request : %s" % data)
        try:

            response = requests.post('http://10.253.0.211/sltServices/ocs/integration/offering', data=json.dumps(data),
                                     headers=headers,auth=auth)

            loggeroffer.info("Response Code: %s" % response.status_code)
            resmsg = response.json()
            print(resmsg)
            #responsedata = {"data": resmsg['data']}
            loggeroffer.info("Response : %s" % resmsg)
            return resmsg

        except Exception as e:
            #print("Exception : %s" % traceback.format_exc())
            loggeroffer.info("Exception : %s" % e)

class OCSadjustment:

    def OCS_adjustment(self, adjAmount, adjType):

        data = {
            "requestHeader": {
                "operationType": "ADJUST_ACC",
                "requestedBy": "slt",
                "systemName": "SLT_OCS_INT"
            },
            "primaryIdentity": self,
            "adjAmount": adjAmount,
            "adjType": adjType,
            "remark":"Adjusted due to OCS Addon error from MY_SLT app"
        }

        print (data)
        loggeroffer.info("Request : %s" % data)
        try:

            response = requests.post('http://10.253.0.211/sltServices/ocs/integration/adjustment', data=json.dumps(data),
                                     headers=headers,auth=auth)

            loggeroffer.info("Response Code: %s" % response.status_code)
            resmsg = response.json()
            print(resmsg)
            #responsedata = {"data": resmsg['data']}
            loggeroffer.info("Response : %s" % resmsg)
            return resmsg

        except Exception as e:
            print("Exception : %s" % e)
            loggeroffer.info("Exception : %s" % e)


def getPackageprice(pkg_id):
    with open('pcrf/mapping.json') as f:
        data = json.load(f)
        for pkg in data['packages_list']:
            if pkg['offeringID'] == str(pkg_id):
                return pkg['pricewithTax']
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

# Modify Routes
api.add_resource(getDetails, const.APP_ROUTE_MAPPING)

#offer
api.add_resource(offerRecharge, const.APP_ROUTE_OFFER)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=20001)
