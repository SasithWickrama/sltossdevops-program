import json
from datetime import datetime

import requests

import const
import db
from log import Logger
from sms import Sendsms

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

def getPackageAll(pkg_id):
    with open('pcrf/mapping.json') as f:
        data = json.load(f)
        for pkg in data['packages_list']:
            if pkg['offeringID'] == str(pkg_id):
                return pkg

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


class getNumber:
    def clarityDb(self):
        try:
            conn = db.DbConnection.dbconnClarity("")
            print(conn)
            result = {}
            if self is not None:
                    parmList = [self,'INSERVICE','SUSPENDED','CUSTOMER CONTACT NO','CUSTOMER CONTACT']
                    sql = 'SELECT C.CIRT_DISPLAYNAME,C.CIRT_SERT_ABBREVIATION,C.CIRT_STATUS ,SA.SATT_ATTRIBUTE_NAME,SA.SATT_DEFAULTVALUE FROM CIRCUITS C, SERVICES_ATTRIBUTES SA WHERE CIRT_DISPLAYNAME = :1 AND CIRT_SERV_ID = SATT_SERV_ID and CIRT_STATUS in (:2,:3) AND SATT_ATTRIBUTE_NAME IN (:4,:5)'
                    c = conn.cursor()
                    #c.execute(sql,{'value':self})
                    c.execute(sql,parmList)
                    results = c.fetchall()
                    print("results:", results)
                    # Get the row count
                    row_count = len(results)

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

            getpkgall = getPackage(data['offeringID'])

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

                    #====SMS====
                    msg = "You have successfully activated the "+getpkgall['packageName'] + ", valid for "+ getpkgall['validPeriod']+" days. To check data balance, use the MySLT App or visit https://myslt.slt.lk/"
                    getmobile =getMobile(data['orderObjectKey'])
                    if getmobile == 'No data found':
                        logger.info("mobile : %s" % ref + " - " + getmobile)
                    else:
                        logger.info("mobile : %s" % ref + " - " + getmobile)
                        smsdata = {"tpno": getmobile, "msg": msg}
                        if getmobile[0:1] == '07' and len(getmobile) == '10':
                            Sendsms.sendSms(smsdata, ref)

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
                            totalUnusedAmount = i['totalUnusedAmount']
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

                                        #====SMS====
                                        msg = "Dear Customer, your Home Broadband account "+data['orderObjectKey']+" has only "+totalUnusedAmount+"MB left from your "+unitType+" pack. Activate a Data Add-on pack to enjoy the benefits"
                                        getmobile =getMobile(data['orderObjectKey'])
                                        if getmobile == 'No data found':
                                            logger.info("mobile : %s" % ref + " - " + getmobile)
                                        else:
                                            logger.info("mobile : %s" % ref + " - " + getmobile)
                                            smsdata = {"tpno": getmobile, "msg": msg}
                                            if getmobile[0:1] == '07' and len(getmobile) == '10':
                                                Sendsms.sendSms(smsdata, ref)



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


    def chnageSubStatus(data,ref):

        dataOcs =   {"requestHeader": {
                "operationType": "QUERY_STATUS",
                "requestedBy": "slt",
                "systemName": "SLT_OCS_INT"
            },
            "primaryIdentity": data["orderObjectKey"][1:10]
        }

        createresponse = requests.post('http://10.253.0.211/sltServices/ocs/integration/query',auth=('SLTUSR', 'SLTPW'),data=json.dumps(dataOcs))
        resmsg = json.loads(createresponse.text)
        logger.info("OCS Response : %s" % ref + " - " + str(resmsg))

        rcode= resmsg['resultHeader']['resultCode']
        if rcode == '0':

            curIndex = resmsg['QueryCustomerInfoResult']['Subscriber']['LifeCycleDetail']['CurrentStatusIndex']

            for i in resmsg['QueryCustomerInfoResult']['Subscriber']['LifeCycleDetail']['LifeCycleStatus']:
                if i['StatusIndex'] == curIndex:
                    timestamp = int(i['StatusExpireTime'])
                    print(timestamp)
                    print(type(timestamp))
                    datetime_obj = datetime.strptime(i['StatusExpireTime'], "%Y%m%d%H%M%S")

                    #====SMS====
            msg = "Dear Customer, the validity of connection 94"+data['orderObjectKey'][1:10]+" (registered under your ID) will expire on "+datetime_obj+". Reload to continue services. Visit https://myslt.slt.lk/ "
            getmobile =getMobile(data['orderObjectKey'])
            if getmobile == 'No data found':
                logger.info("mobile : %s" % ref + " - " + getmobile)
            else:
                logger.info("mobile : %s" % ref + " - " + getmobile)
                smsdata = {"tpno": getmobile, "msg": msg}
                if getmobile[0:1] == '07' and len(getmobile) == '10':
                    Sendsms.sendSms(smsdata, ref)

        else:
            return {'result': 'error', 'description': resmsg, 'data': data}

    def Recharge(data,ref):
        logger.info("OCS Request : %s" % ref + " - " + str(data))
        dataOcs =   {"requestHeader": {
            "operationType": "QUERY_STATUS",
            "requestedBy": "slt",
            "systemName": "SLT_OCS_INT"
        },
            "primaryIdentity": data["orderObjectKey"][1:10]
        }

        createresponse = requests.post('http://10.253.0.211/sltServices/ocs/integration/query',auth=('SLTUSR', 'SLTPW'),data=json.dumps(dataOcs))
        resmsg = json.loads(createresponse.text)
        logger.info("OCS Response : %s" % ref + " - " + str(resmsg))

        rcode= resmsg['resultHeader']['resultCode']
        logger.info("OCS Response : %s" % ref + " - " + str(rcode))
        if rcode == '0':

            curIndex = resmsg['QueryCustomerInfoResult']['Subscriber']['LifeCycleDetail']['CurrentStatusIndex']
            logger.info("OCS Response : %s" % ref + " - " + str(curIndex))
            for i in resmsg['QueryCustomerInfoResult']['Subscriber']['LifeCycleDetail']['LifeCycleStatus']:
                if i['StatusIndex'] == curIndex:
                    timestamp = int(i['StatusExpireTime'])
                    datetime_obj = datetime.strptime(i['StatusExpireTime'], "%Y%m%d%H%M%S")


                    #====SMS====
                    try:
                        #rechargeAmount = round((data['rechargeAmount'] / 100 ), 2)
                        #balanceAfterRecharge = round((data['balanceAfterRecharge'] / 100 ), 2)
                        rechargeAmount =data['rechargeAmount']
                        balanceAfterRecharge =data['balanceAfterRecharge']
                        msg = "Dear customer, your account "+'94'+data['orderObjectKey'][1:10]+" has been recharged with Rs."+str(rechargeAmount)+". Your new balance is Rs."+str(balanceAfterRecharge)+" & will expire on "+str(datetime_obj)
                        logger.info("sms msg : %s" % ref + " - " + str(msg))

                        getmobile = getNumber.clarityDb(data['orderObjectKey'])
                        logger.info("mobile : %s" % ref + " - " + str(getmobile))
                        if getmobile == 'No data found':
                            logger.info("mobile : %s" % ref + " - " + getmobile)
                        else:
                            logger.info("mobile : %s" % ref + " - " + getmobile)
                            smsdata = {"tpno": getmobile, "msg": msg}
                            logger.info("mobile : %s" % ref + " - " + str(smsdata))
                            if getmobile[0:1] == '07' and len(getmobile) == '10':
                                Sendsms.sendSms(smsdata, ref)
                    except Exception as e:
                        logger.info("Exception : %s" % ref + " - " + str(e))

        else:
            return {'result': 'error', 'description': resmsg, 'data': data}


