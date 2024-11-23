import json
import requests

import const
from log import Logger

logger = Logger.getLogger('pcrf', 'logs/pcrf')


def pcrfToken(data):
    headers = {'subscriberid': data}
    try:
        response = requests.get(
            const.PCRF_TOKEN_URL, headers=headers)

        resmsg = json.loads(response.text)

        # if resmsg['subscriberToken'] is not None:
        if response.status_code == 200:
            responsedata = {"result": "success", "token": resmsg['subscriberToken']}
        else:
            responsedata = {"result": "error", "msg": resmsg['message']}
    except Exception as e:
        responsedata = {"result": "error", "msg": e}

    return responsedata


def pcrfVasData(data):
    headers = {'subscriberid': data}
    try:
        response = requests.get(
            const.PCRF_ADDON_VASDATA_URL, headers=headers)

        resmsg = json.loads(response.text)

        # if resmsg['subscriberToken'] is not None:
        if response.status_code == 200:
            responsedata = {"result": "success", "usage": resmsg['usageDetails']}
        else:
            responsedata = {"result": "error", "msg": resmsg['message']}
    except Exception as e:
        responsedata = {"result": "error", "msg": e}

    return responsedata


def getPackage(pkg_id):
    with open('pcrf/mapping.json') as f:
        data = json.load(f)
        for pkg in data['packages_list']:
            if pkg['offeringID'] == str(pkg_id):
                return pkg['pcrfID']

def getDeletePackage(accountType):
    with open('pcrf/mapping.json') as f:
        data = json.load(f)
        for pkg in data['packages_list']:
            if pkg['accountType'] == str(accountType):
                return pkg['pcrfName']

def getfreeUnitType(accountType):
    with open('pcrf/mapping.json') as f:
        data = json.load(f)
        for pkg in data['packages_list']:
            if pkg['pcrfID'] == str(accountType):
                return pkg['freeUnitType']

class Pcrf:

    def pcrfAddonCreate(data, ref ):

        try:
            logger.info("Token Request : %s" % ref + " - " + str(data))
            result = pcrfToken('94'+data['orderObjectKey'][1:10])
            logger.info("Token Response : %s" % ref + " - " + str(result))

        except Exception as e:
            responsedata = {"result": "error", "msg": ref +" - Connection Issue"}
            logger.error("Return : %s" % ref + " - " + str(responsedata))
            return responsedata


        try:
            getpkg = getPackage(data['offeringID'])

            if getpkg is not None:
                headers = {'subscriberid': result['token'],
                           'Content-Type': 'application/json'}

                payload = {"packageId": getpkg, "commitUser": "OCS", "channel": "OCS"}
                response = requests.post(
                    const.PCRF_ADDON_CREATE_URL, headers=headers, data=json.dumps(payload))
                logger.info("Request : %s" % ref + " - " + str(payload))

                resmsg = json.loads(response.text)
                logger.info("Response : %s" % ref + " - " + str(resmsg))

                # if resmsg['status'] == 'SUCCESS':
                if response.status_code == 200:
                    responsedata = {"result": "success", "description": ref+" - "+resmsg['message'], 'data': data}
                    logger.info("Return : %s" % ref + " - " + str(responsedata))
                else:
                    responsedata = {"result": "error", "description": ref+" - "+resmsg['message'], 'data': data}
                    logger.info("Return : %s" % ref + " - " + str(responsedata))
            else:
                responsedata = {"result": "error", "description": ref+" - invalid offer id", 'data': data}
                logger.info("Return : %s" % ref + " - " + str(responsedata))

        except Exception as e:
            responsedata = {"result": "error", "description": ref+" - "+str(e), 'data': data}
            logger.info("Return : %s" % ref + " - " + str(responsedata))

        return responsedata


    def pcrfAddonDelete(data,ref):

        data['ref'] = ref

        dataOcs = {"requestHeader": {
            "operationType": "QUERY_FREE_UNITS",
            "requestedBy": "slt",
            "systemName": "SLT_OCS_INT"
        },
            "primaryIdentity": data["orderObjectKey"][1:10]
        }

        unitType = getfreeUnitType(data['accountType'])

        try:
            logger.info("OCS Request : %s" % ref + " - " + str(dataOcs))
            logger.info("unitType : %s" % ref + " - " + str(unitType))
            curValue = True

            createresponse = requests.post('http://10.253.0.211/sltServices/ocs/integration/query',auth=('SLTUSR', 'SLTPW'),data=json.dumps(dataOcs))
            resmsg = json.loads(createresponse.text)
            logger.info("OCS Response : %s" % ref + " - " + str(resmsg))

            rcode= resmsg['resultHeader']['resultCode']
            if rcode == '0':
                offerZero =set()
                if "QueryCustomerInfoResult" in resmsg:
                    for i in resmsg['QueryCustomerInfoResult']['subscriber']['freeUnitInfo']['freeUnitItem']:
                        if(i['freeUnitTypeName'] == unitType):
                            for item in i['itemDetail']:
                                if str(item['currentAmount']) > '0':
                                    curValue = False

                    logger.info("PCRF Token Request : %s" % ref + " - " + str(data))
                    resultPcrfToken = pcrfToken('94'+data['orderObjectKey'][1:10])
                    logger.info("PCRF Token Response : %s" % ref + " - " + str(resultPcrfToken))


                    resultPcrfVas = pcrfVasData(resultPcrfToken['token'])
                    logger.info("PCRF VAS Response : %s" % ref + " - " + str(resultPcrfVas))


                    if resultPcrfVas['result'] == 'success':
                        if "usage" in resultPcrfVas:
                            for val in resultPcrfVas['usage']:
                                if val['subscriptionid'] == 'P_VB_Q_OM_PREPAID_30GB' or 'P_VB_PRE_SMYT':
                                
                                    logger.info(" VAS val : %s" % ref + " - " + str(val['subscriptionid']) + " - " + str(val['timestamp']))
                                    
                                    if str(val['timestamp']) is not None:
                                        headers = {'subscriberid': resultPcrfToken['token'],
                                                   'Content-Type': 'application/json'}

                                        payload = {"timestamp": str(val['timestamp']), "subscriptionid": val['subscriptionid']}
                                        response = requests.post(
                                            const.PCRF_ADDON_DELETE_URL, headers=headers, data=json.dumps(payload))
                                        logger.info("Request : %s" % ref + " - " + str(payload))

                                        resmsg = json.loads(response.text)
                                        logger.info("Response : %s" % ref + " - " + str(resmsg))
                                    else:
                                        return {'result': 'error', 'description': 'Invalid Request', 'data': data}
                                        logger.info("Return : %s" % ref + " - " + str(responsedata))                                       

                    return {'result': resultPcrfVas, 'description': curValue, 'data': unitType}
                else:
                    return {'result': 'error', 'description': 'Invalid Request', 'data': data}
            else:
                return {'result': 'error', 'description': resmsg, 'data': data}

        except Exception as e:
            responsedata = {"result": "error", "msg": ref +" - Connection Issue"}
            logger.error("Return : %s" % ref + " - " + str(responsedata))
            return responsedata
