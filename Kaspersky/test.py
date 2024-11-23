import json

from flask import Flask, request, jsonify
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


# class Employees_Name(Resource):
#     def get(self, employee_id):
#         conn = db_connect.connect()
#         query = conn.execute("select * from employees where EmployeeId =%d "  %int(employee_id))
#         result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
#         return jsonify(result)

# class getVal(Resource):
#     def get(self,ename):
#
#         id= ename[1]
#         return ename
#
#        # return jsonify("hello "+ ename + "how are you")
#
#
# api.add_resource(getVal, '/pythonrest/getval/<ename>') # Route_3

class getReq(Resource):
    def get(self):
        data={'about'  : 'hello'}
        return jsonify(data)

    def put(self):
        return jsonify({'message ':'data updated'})

    def post(self):
        data = request.get_json()
        subid= data['Customer']
        con =subid['Contacts']
        conname = con['CompanyName']

        return conname, 201



api.add_resource(getReq,'/flaskapi/createsub/')


if __name__ == '__main__':
    app.run(debug=True, port=5002)

