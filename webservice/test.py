# class_list = dict()
# data = input('Enter name & score separated by ":" ')
# temp = data.split(':')
# class_list[temp[0]] = int(temp[1])
#
# # Displaying the dictionary
# for key, value in class_list.items():
#     print('Name: {}, Score: {}'.format(key, value))
import json

import requests

headers = {
    'Content-type': 'application/json',
    'Accept': 'application/json'}

data = {"username": "012583", "password": "Aadp$19870120"}

createresponse = requests.post('https://ebsmobileapp.slt.com.lk/API/v1/employee/login',
                               data=json.dumps(data),
                               headers=headers)
responce = createresponse.json()
print(responce['authtoken'])
print(responce['person_id'])

data2 = {"username": "012583", "personid": responce['person_id']}


headers = {
    'username': '012583',
    'personid': str(responce['person_id']),
    'Authorization': 'Bearer '+str(responce['authtoken'])
}

createresponse2 = requests.get('https://ebsmobileapp.slt.com.lk/API/v1/employee/leavebalance',headers=headers)
responce2 = createresponse2.json()
print(responce2)
