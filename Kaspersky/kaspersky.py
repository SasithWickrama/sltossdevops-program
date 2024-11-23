import requests
import json
import simplejson as json

from pyasn1.compat.octets import null
from cryptography.hazmat.primitives.serialization import pkcs12
from cryptography.hazmat.primitives import serialization

with open("Kaspersky/c412341de164496c869b1ee1beb51bc099bb1940f6a44fcb8c44f2b32cec6e77.pfx", "rb") as f:
    private_key, certificate, additional_certificates = pkcs12.load_key_and_certificates(f.read(), b"89)iopJKL")


    key = open("key.pem", 'wb')
    cert = open("cert.pem", 'wb')
    key.write(
        private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )
    )
    key.flush()
    cert.write(
        certificate.public_bytes(serialization.Encoding.PEM),
    )
    cert.flush()

payload = {
    "BillingPlan":"Yearly",
    "Sku":"KL48633A*MG",
    "Quantity":10,
    "Expiration":null,
    "Customer":{
        "Contacts":{
            "CompanyName":"Paramount",
            "Email":"test.ya.ru",
            "Phone":"123456",
            "CustomerCode":"1122"
        },
        "Address":{
            "AddressLine1":"10300 Broadway st.",
            "AddressLine2":"smh",
            "City":"New York",
            "State":"New York",
            "Zip":"10025",
            "Country":"USA"
        }
    },
    "Distributor":{
        "Partner":"SLT",
        "Reseller":"TE27PT00"
    },
    "Comment":"It's just test!",
    "DeliveryEmail":"prabodha@slt.com.lk"
}

payloadMod = {"SubscriptionId":"d6099078-a655-47b0-a12c-c95729302a49",
              "Quantity":20}

payloadCancle = {
    "SubscriptionId":"1afe1433-a38e-4c79-8503-8d5687b44eb1"}

cert = ("cert.pem", "key.pem")

headers = {
    'Content-type':'application/json',
    'Accept':'application/json'
}
cert = ("cert.pem", "key.pem")

createresponse = requests.post('https://api.demo.korm.kaspersky.com/Subscriptions/v2.0/api/Subscription/create',
                  cert=cert,
                  data=json.dumps(payload),
                  headers=headers)

print("Status Code " + str(createresponse.status_code))
print("Response " + str(createresponse.json()))

resmsg=  json.loads(createresponse.text)
print(resmsg['Message'])



# modifyresponse = requests.post('https://api.demo.korm.kaspersky.com/Subscriptions/v2.0/api/Subscription/modifyexpiration',
#                   cert=cert,
#                   json=payloadMod,
#                   headers=headers)
#
# print("Status Code " + str(modifyresponse.status_code))
# print("Response " + str(modifyresponse.json()))

# hardcancleresponse = requests.post('https://api.demo.korm.kaspersky.com/Subscriptions/v2.0/api/Subscription/hardcancel',
#                   cert=cert,
#                   json=payloadMod,
#                   headers=headers)
# print("Status Code " + str(hardcancleresponse.status_code))
# print("Response " + str(hardcancleresponse.json()))
