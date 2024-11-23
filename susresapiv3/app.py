from flask import Flask, request
from flask_restful import Api, Resource
from eprov.eprov import Eprov
from eprov.recordInputSchema import Validate


app = Flask(__name__)
api = Api(app)

class ProvRequest(Resource):
    def post(self):
        data = request.get_json()
        result = Validate.validateReq(data)
        if result == 'success':
            return Eprov.prov_request(data)
        else:
            return result

class GetData(Resource):
    def post(self):
        data = request.get_json()
        return Eprov.get_records(data)

# EPROV Routes
api.add_resource(ProvRequest, '/api/provreq/')

api.add_resource(GetData, '/api/getData/')

if __name__ == '__main__':
    app.run(debug=True, port=5002)
