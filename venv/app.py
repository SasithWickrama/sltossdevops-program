import requests

r = requests.post('https://httpbin.org/post')
print(r.status_code)
