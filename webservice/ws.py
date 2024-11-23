import xml.etree.ElementTree as ET
import zeep
import requests

# wsdl = 'http://172.25.37.196:8080/Smssystem/smsSending?WSDL'
# client = zeep.Client(wsdl=wsdl)
# print(client.service.smsdirectx('0710959907', 'hi probo', 'OSS', 'SLTCMS', '!23qweASD'))

# api-endpoint


# query = {'sid': '012583', 'appversion': '1.01'}
# response = requests.post('https://serviceportal.slt.lk/ApiGis/public/api/checkVersion?', data=query,
#                          allow_redirects=True)
# print(response.json())  # This method is convenient when the API returns JSON

# SOAP request URL

userid, locationid,storeid = '', '' , ''

url = "https://vendorapi.etpos.lk/soap/merchant/server"

# headers
headers = {
    'Content-Type': 'application/xml'
}

xmlfile = open('register.xml', 'r')
body = xmlfile.read()

# POST request
response = requests.request("POST", url, headers=headers,
                            data=body.format(name='SLT', email='slt51@slt.com.lk', company='SLT', telephone='',
                                             mobile='0710123456', username='26slttest',
                                             password='abcd123', confirmedPassword='abcd123', registrantName='',
                                             registrantRelation='', registrantMobile='',
                                             id='910940245V', address='Colombo', no_of_stores=3, plan='basic_monthly'))

# prints the response
print(response.text)

root = ET.fromstring(response.content)

if response.status_code == 200:
    for child in root.iter('userId'):
        userid = child.text
        print('userId ' + userid)

        xmlfiletype = open('type.xml', 'r')
        bodytype = xmlfiletype.read()

        responsetype = requests.request("POST", url, headers=headers,
                                        data=bodytype.format(type='Warehouse', userid=userid))

        print(responsetype.text)

        roottype = ET.fromstring(responsetype.content)

        if responsetype.status_code == 200:
            for child in roottype.iter('id'):
                locationid = child.text
                print('id ' + locationid)

                xmlfilestore = open('store.xml', 'r')
                bodystore = xmlfilestore.read()

                responsestore = requests.request("POST", url, headers=headers,
                                                 data=bodystore.format(name='SLT', contactno='0710123456',
                                                                       email='slt52@slt.com.lk', fax='',
                                                                       locationType=locationid, userid=userid,
                                                                       category='baby_products',
                                                                       addressLine1='No 123. ', city='Colombo 04',
                                                                       country='Sri Lanka',
                                                                       addressLine2='Galle Road,Colombo 04',
                                                                       state='Colombo',
                                                                       postalCode='00400'))

                print(responsestore.text)

                rootstore = ET.fromstring(responsestore.content)

                if responsetype.status_code == 200:
                    for child in roottype.iter('locationId'):
                        storeid = child.text
                        print('storeid ' + storeid)

                else:
                    for child in roottype.iter('faultstring'):
                        print('faultstring ' + child.text)
        else:
            for child in roottype.iter('faultstring'):
                print('faultstring ' + child.text)

else:
    for child in root.iter('faultstring'):
        print('faultstring ' + child.text)
