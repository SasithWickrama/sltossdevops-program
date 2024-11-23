import datetime
import os
import re
from datetime import datetime
import const
import requests
import subprocess

cdate = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

class Suspend:
    def voiceSuspend(self):
        try:
            const.logsusvoice.info(self['LOGREF'] + "  " + "========================= Start Voice Suspend: =========================")
            const.logsusvoice.info(self['LOGREF'] + "  " + str(self))

            if self['ORDER_TYPE'] == 'MODI-PARTIAL SUSPEND':

                xmlfile = open('files/BAR_OUTGOING_CALL.xml', 'r')
                data = xmlfile.read()

                for key in self:
                    value = self[key]
                    data = data.replace(key, str(value))

                response = requests.request("POST", const.voiceend, data=data)

                const.logsusvoice.info(self['LOGREF'] + "  " + "==================== Request Voice Outgoing BAR : ====================")
                const.logsusvoice.info(self['LOGREF'] + "  " + str(response.request.body))
                const.logsusvoice.info(self['LOGREF'] + "  " + "==================== Response Voice Outgoing BAR : ====================")
                const.logsusvoice.info(self['LOGREF'] + "  " + str(response.text))

                ResultCode = re.findall("<ns1:ResultCode>(.*?)</ns1:ResultCode>", str(response.content))
                ResultDesc = re.findall("<ns1:ResultDesc>(.*?)</ns1:ResultDesc>", str(response.content))

                const.logsusvoice.info(self['LOGREF'] + "  " + str(ResultCode[0]) + '#' + str(ResultDesc[0]))
                const.logsusvoice.info(self['LOGREF'] + "  " + "========================= End Voice Suspend: =========================")
                return str(ResultCode[0])

            if self['ORDER_TYPE'] == 'SUSPEND':
                xmlfile = open('files/BAR_OUTGOING_CALL.xml', 'r')
                data = xmlfile.read()

                for key in self:
                    value = self[key]
                    data = data.replace(key, str(value))

                response = requests.request("POST", const.voiceend, data=data)

                const.logsusvoice.info(self['LOGREF'] + "  " + "==================== Request Voice Outgoing BAR: ====================")
                const.loggersus.info(self['LOGREF'] + "  " + str(response.request.body))
                const.logsusvoice.info(self['LOGREF'] + "  " + "==================== Response Voice Outgoing BAR: ====================")
                const.loggersus.info(self['LOGREF'] + "  " + str(response.text))

                ResultCode = re.findall("<ns1:ResultCode>(.*?)</ns1:ResultCode>", str(response.content))
                ResultDesc = re.findall("<ns1:ResultDesc>(.*?)</ns1:ResultDesc>", str(response.content))

                const.loggersus.info(self['LOGREF'] + "  " + str(ResultCode[0]) + '#' + str(ResultDesc[0]))

                if ResultCode[0] == '0':

                    xmlfile = open('files/BAR_INCOMING_CALL.xml', 'r')
                    datainc = xmlfile.read()

                    for key in self:
                        value = self[key]
                        datainc = datainc.replace(key, str(value))

                    responseinc = requests.request("POST", const.voiceend, data=datainc)

                    const.logsusvoice.info(self['LOGREF'] + "  " + "==================== Request Voice Incoming BAR: ====================")
                    const.logsusvoice.info(self['LOGREF'] + "  " + str(responseinc.request.body))
                    const.logsusvoice.info(self['LOGREF'] + "  " + "==================== Response Voice Incoming BAR: ====================")
                    const.logsusvoice.info(self['LOGREF'] + "  " + str(responseinc.text))

                    ResultCodeinc = re.findall("<ns1:ResultCode>(.*?)</ns1:ResultCode>", str(responseinc.content))
                    ResultDescinc = re.findall("<ns1:ResultDesc>(.*?)</ns1:ResultDesc>", str(responseinc.content))

                    result = Suspend.crbt(self)

                    const.logsusvoice.info(self['LOGREF'] + "  " + str(ResultCodeinc[0]) + '#' + str(ResultDescinc[0]) + '#' + str(result))
                    const.logsusvoice.info(self['LOGREF'] + "  " + "========================= End Voice Suspend: =========================")
                    return str(ResultCodeinc[0])
                else:
                    const.logsusvoice.info(self['LOGREF'] + "  " + "========================= End Voice Suspend: =========================")
                    return str(ResultCode[0])

        except Exception as e:
            const.logsusvoice.error(self['LOGREF'] + "  " + str(e))
            const.logsusvoice.info(self['LOGREF'] + "  " + "========================= End Voice Suspend: =========================")
            return str(e)

    def crbt(self):
        try:
            const.logsusvoice.info(self['LOGREF'] + "  " + "========================= Start CRBT: =========================")

            xmlfile = open('files/voice/CallBackStatus.xml', 'r')
            headers = {'content-type': 'text/xml'}
            data = xmlfile.read()

            for key in self:
                value = self[key]

                data = data.replace(key, str(value))

            response = requests.request("POST", const.crbt, headers=headers, data=data)
            const.logsusvoice.info(self['LOGREF'] + "  " + str(response.request.body))
            const.logsusvoice.info(self['LOGREF'] + "  " + "==================== Response CRBT: ====================")
            const.logsusvoice.info(self['LOGREF'] + "  " + str(response.text))
            const.logsusvoice.info(self['LOGREF'] + "  " + "========================= End CRBT: =========================")

            ResultCode = re.findall("<return xsi:type=\"xsd:string\">(.*?)</return>", str(response.content))
            return ResultCode[0]

        except Exception as e:
            const.logsusvoice.error(self['LOGREF'] + "  " + str(e))
            const.logsusvoice.info(self['LOGREF'] + "  " + "========================= End CRBT: =========================")

    def broadbandSuspend(self):
        # repdesc = 'Suspend using SR system on '+cdate
        # # LDAP
        # xmlfile = open('files/suspend.ldif', 'r')
        # body = xmlfile.read()
        # indata = {"uidrep": self['MSISDN'], "repdesc": repdesc}
        # for key in indata:
        #     value = indata[key]
        #     body = body.replace(key, value)
        #
        # print(body)
        #
        # filename = self['MSISDN']+'.ldif'
        # fh = open(filename, 'w')
        # fh.write(body)
        # fh.close()
        #
        # cmdexe = subprocess.Popen('cmd /c "ldapmodify -h '+const.ldapip+' -D \"uid='+const.ldapusr+',cn=config\" -w \"'+const.ldappwd+'\" -f '+filename+'"', shell=True, stdout=subprocess.PIPE)
        # result = cmdexe.stdout.readlines()
        #
        # const.loggersus.info(self['LOGREF'] + "  " + "Response LDAP: =================================")
        #
        # for line in result:
        #     print(line.decode('UTF-8'))
        #     const.loggersus.info(self['LOGREF'] + "  " + str(line.decode('UTF-8')))
        #
        # os.remove(filename)

        # PCRF
        try:
            const.logsusbb.info(self['LOGREF'] + "  " + "========================= Start BB Suspend: =========================")
            const.logsusbb.info(self['LOGREF'] + "  " + str(self))

            xmlfile = open('files/bb/blockSubscriber.xml', 'r')
            headers = {'content-type': 'text/xml'}
            data = xmlfile.read()

            for key in self:
                value = self[key]

                data = data.replace(key, str(value))

            response = requests.request("POST", const.pcrf, headers=headers, data=data)
            const.logsusvoice.info(self['LOGREF'] + "  " + "==================== Request BB : ====================")
            const.logsusiptv.info(self['LOGREF'] + "  " + str(response.request.body))
            const.logsusiptv.info(self['LOGREF'] + "  " + "==================== Response BB : ====================")
            const.logsusiptv.info(self['LOGREF'] + "  " + str(response.text))

            ResultCode = re.findall("<return>(.*?)</return>", str(response.content))

            const.logsusbb.info(self['LOGREF'] + "  " + str(ResultCode[0]) )
            const.logsusbb.info(self['LOGREF'] + "  " + "========================= End BB Suspend: =========================")
            return ResultCode[0]

        except Exception as e:
            const.logsusbb.error(self['LOGREF'] + "  " + str(e))
            const.logsusbb.info(self['LOGREF'] + "  " + "========================= End BB Suspend: =========================")
            return str(e)

    def iptvSuspend(self):
        try:
            const.logsusiptv.info(self['LOGREF'] + "  " + "========================= Start IPTV Suspend: =========================")
            const.logsusiptv.info(self['LOGREF'] + "  " + str(self))

            xmlfile = open('files/iptv/IPTV_SUNT_SUSPEND.xml', 'r')
            data = xmlfile.read()

            for key in self:
                value = self[key]
                data = data.replace(key, str(value))

            response = requests.request("POST", const.iptvend, data=data)

            const.logsusvoice.info(self['LOGREF'] + "  " + "==================== Request IPTV : ====================")
            const.logsusiptv.info(self['LOGREF'] + "  " + str(response.request.body))
            const.logsusiptv.info(self['LOGREF'] + "  " + "==================== Response IPTV : ====================")
            const.logsusiptv.info(self['LOGREF'] + "  " + str(response.text))

            Result = re.findall("<ax225:abstractServiceObjects xsi:type=\"ax222:AbstractServiceObject\">(.*?)</ax225:abstractServiceObjects>", str(response.content))
            ResultCode = re.findall("<ax222:value>(.*?)</ax222:value>", str(Result[0]))
            ResultDesc = re.findall("<ax222:value>(.*?)</ax222:value>", str(Result[1]))

            const.logsusiptv.info(self['LOGREF'] + "  " + str(ResultCode[0]) + '#' + str(ResultDesc[0]))
            const.logsusiptv.info(self['LOGREF'] + "  " + "========================= End IPTV Suspend: =========================")
            return str(ResultCode[0])

        except Exception as e:
            const.logsusiptv.error(self['LOGREF'] + "  " + str(e))
            const.logsusiptv.info(self['LOGREF'] + "  " + "========================= End IPTV Suspend: =========================")
            return str(e)