import requests
import json

serverToken = 'AAAAMNchzVw:APA91bGzR8TnsBYAkycI8xsrXE1kUrHYRJEIHtJ-TJ3G-hj6nHwuDrtqQ7HUbNGqA4uf4qWcuEiuzDMNdqM7ew8MDv0QIEnLuIWtW5j8CNNj1ANhv9GhVkGodGIu6DUj-BqaucUxPRNt'
deviceToken = 'ezRn6DKqRj-dHg_6w0s2hp:APA91bGFVrjfML8QEWkj8I6pbD7LV2ze_VkZeb4KBPVq156_Oghcg6_Ppmzfadi9yGYbdqi_2ItPglqr_qdp4GnIcd5BBN7hYQ-YKQ5eAh9xn8a3R0-p84Eexy6ntCE9wl9WFIr7O2F1'

headers = {
    'Content-Type': 'application/json',
    'Authorization': 'key=' + serverToken,
}

body = {
    'notification': {'title': 'Sending push form python script',
                     'body': 'New Message'
                     },
    'to':
        deviceToken,
    'priority': 'high',
    #   'data': dataPayLoad,
}
response = requests.post("https://fcm.googleapis.com/fcm/send",headers = headers, data=json.dumps(body))
print(response.status_code)

print(response.json())