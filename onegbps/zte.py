#!F:\Python\Python39\python.exe
import re
import traceback
import requests
from log import getLogger
import xml.etree.ElementTree as ET

endpoint = "http://10.64.73.49:9090/axis2/services/NeManagementService/";

proxies = {
    "http": None,
    "https": None,
}

class Ztecreate:
    def zteVlan(self, indata, inval, inval2):
        #loggerZte = getLogger(self['PENO'] + '_ZTE', 'F:\\xampp\\htdocs\\IMS\\dbFunction\\ONEGBPS\\logs\\' + self['PENO'])
        try:
            xmlfile = open('F:\\xampp\\htdocs\\IMS\\dbFunction\\ONEGBPS\\files\\zte\\' + self, 'r')
            data = xmlfile.read()

            for key in indata:
                value = indata[key]
                data = data.replace(key, str(value))

            response = requests.request("POST", endpoint,data=data, proxies=proxies)

            count = 1
            data = {}
            root = ET.fromstring(response.content)

            for resultc in root.iter('statusCode'):
                ResultCode = resultc.text

            for resultd in root.iter('statusDesc'):
                ResultDesc = resultd.text

            for record in root.iter('record'):
                count = count + 1
                for param in record.iter('param'):
                    count = count + 1
                    for name in param.iter('name'):
                        if name.text != 'totalrecord':
                            count = count + 1
                            name = name.text
                            for value in param.iter('value'):
                                if count == 3:
                                    value = value.text
                                    if value == inval:
                                        if inval == 'Entree':
                                            data['EVLAN'] = value2
                                        elif inval == 'IPTV_SVLAN':
                                            data['IPSV'] = value2
                                        else:
                                            data[value] = value2
                                    if value == inval2:
                                        if inval2 == 'IPTV':
                                            data['IPTVLAN'] = value2
                                        else:
                                            data[value] = value2
                                if count == 4:
                                    value2 = value.text

                                count = 1
            #print(data)
            if (ResultCode == '0'):
                return data
            else:
                return str(ResultCode) + '#' + str(ResultDesc)

        except Exception as e:
            return e

    def zteCreate(self, indata):
        loggerZte = getLogger(indata['PENO'] + '_ZTE', 'F:\\xampp\\htdocs\\IMS\\dbFunction\\ONEGBPS\\logs\\' + indata['PENO'])

        try:
            xmlfile = open('F:\\xampp\\htdocs\\IMS\\dbFunction\\ONEGBPS\\files\\zte\\' + self, 'r')
            data = xmlfile.read()

            for key in indata:
                value = indata[key]
                data = data.replace(key, value)

            response = requests.request("POST", endpoint,data=data, proxies=proxies)

            loggerZte.info(indata["REF_ID"]+"  " +"Start : ============================================================")
            loggerZte.info(indata["REF_ID"]+"  " +"Input Data : "+str(self))
            loggerZte.info(indata["REF_ID"]+"  " +"command xml :"+str(indata))
            loggerZte.info(indata["REF_ID"]+"  " +response.request.body)
            loggerZte.info(indata["REF_ID"]+"  " +"Response : ============================================================")
            loggerZte.info(indata["REF_ID"]+"  " +response.text)

            ResultCode=re.findall("<statusCode>(.*?)</statusCode>", str(response.content))
            ResultDesc=re.findall("<statusDesc>(.*?)</statusDesc>", str(response.content))

            loggerZte.info(indata["REF_ID"]+"  " +str(ResultCode[0]) + '#' + str(ResultDesc[0]))
            loggerZte.info(indata["REF_ID"]+"  " +"End : ============================================================")
            return str(ResultCode[0]) + '#' + str(ResultDesc[0])

        except Exception as e:
            loggerZte.error(indata["REF_ID"]+"  " +str(e))
            loggerZte.info(indata["REF_ID"]+"  " +"End : ============================================================")
            return e

class Ztedelete:
    def zteDelete(self):
        loggerZte = getLogger(self['PENO'] + '_ZTE', 'F:\\xampp\\htdocs\\IMS\\dbFunction\\ONEGBPS\\logs\\' + self['PENO'])
        # FAB DELETE / VOICE DELETE
        try:
            xmlfile = open('F:\\xampp\\htdocs\\IMS\\dbFunction\\ONEGBPS\\files\\zte\\FTTH_DEL_ONU.xml', 'r')
            data = xmlfile.read()

            for key in self:
                value = self[key]
                data = data.replace(key, value)

            response = requests.request("POST", endpoint,data=data, proxies=proxies)

            loggerZte.info(self["REF_ID"]+"  " +"Start Delete: ============================================================")
            loggerZte.info(self["REF_ID"]+"  " +"Input Data : "+str(self))
            loggerZte.info(self["REF_ID"]+"  " +"command xml : FTTH_DEL_ONU.xml")
            loggerZte.info(self["REF_ID"]+"  " +response.request.body)
            loggerZte.info(self["REF_ID"]+"  " +"Response : ============================================================")
            loggerZte.info(self["REF_ID"]+"  " +response.text)

            root = ET.fromstring(response.content)
            for resultc in root.iter('statusCode'):
                ResultCode = resultc.text

            for resultd in root.iter('statusDesc'):
                ResultDesc = resultd.text

            loggerZte.info(self["REF_ID"]+"  " +str(ResultCode) + '#' + str(ResultDesc))
            loggerZte.info(self["REF_ID"]+"  " +"End Delete: ============================================================")
            return str(ResultCode) + '#' + str(ResultDesc)

        except Exception as e:
            loggerZte.error(self["REF_ID"]+"  " +str(e))
            loggerZte.info(self["REF_ID"]+"  " +"End Delete: ============================================================")
            return e

class ZteGetSn:
    def zteGetSn(self, indata):
        loggerZte = getLogger(indata['PENO'] + '_ZTE', 'F:\\xampp\\htdocs\\IMS\\dbFunction\\ONEGBPS\\logs\\' + indata['PENO'])
        try:
            xmlfile = open('F:\\xampp\\htdocs\\IMS\\dbFunction\\ONEGBPS_TEST\\files\\zte\\' + self, 'r')
            data = xmlfile.read()

            for key in indata:
                value = indata[key]
                data = data.replace(key, value)

            response = requests.request("POST", endpoint,data=data, proxies=proxies)

            loggerZte.info(indata["REF_ID"]+"  " +"Start Serial : ============================================================")
            loggerZte.info(indata["REF_ID"]+"  " +"Input Data : "+str(self))
            loggerZte.info(indata["REF_ID"]+"  " +"command xml :"+str(indata))
            loggerZte.info(indata["REF_ID"]+"  " +response.request.body)
            loggerZte.info(indata["REF_ID"]+"  " +"Response : ============================================================")
            loggerZte.info(indata["REF_ID"]+"  " +response.text)


            data = {}
            data['SN'] = ''
            root = ET.fromstring(response.content)

            for resultc in root.iter('statusCode'):
                ResultCode = resultc.text

            for resultd in root.iter('statusDesc'):
                ResultDesc = resultd.text
            print(ResultCode)
            print(ResultDesc)

            for record in root.iter('record'):
                for param in record.iter('param'):
                    for name in param.iter('name'):
                        if name.text == 'LOID':
                            for value in param.iter('value'):
                                data['SN'] = value.text


            loggerZte.info(indata["REF_ID"]+"  " +str(ResultCode[0]) + '#' + str(ResultDesc[0]))
            loggerZte.info(indata["REF_ID"]+"  " +"End Serial: ============================================================")

            if ResultCode == '0':
                return data

            else:
                return str(ResultCode) + '#' + str(ResultDesc)

        except Exception as e:
            loggerZte.error(indata["REF_ID"]+"  " +str(e))
            loggerZte.info(indata["REF_ID"]+"  " +"End Serial: ============================================================")
            return e