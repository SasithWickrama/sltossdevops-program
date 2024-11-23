from functools import wraps
from flask import request, jsonify, make_response
from db import DbConnection
import datetime
import cx_Oracle
import hashlib
import jwt
import const


class Authentication:
    def token_required(self):
        @wraps(self)
        def decorated(*args, **kwargs):
            token = None

            if 'x-access-token' in request.headers:
                token = request.headers['x-access-token']
            if not token:
                return jsonify({'success': 'false', 'message': 'Token is missing!'})
            try:
                data = jwt.decode(token, const.SECRET_KEY, algorithms=["HS256"])
                print(data)
            except:
                return {'message': 'Token is invalid!'}, 401
            return self(*args, **kwargs)

        return decorated

    def login(self):
        if not self or not self.username or not self.password:
            # return make_response({'success': 'false', 'message': 'Authentication Required'}, 401,
            #                      {'WWW-Authenticate': 'Basic realm="Login required!"'})
            return 'Authentication Required'
        hashpwd = hashlib.md5(self.password.encode())

        try:
            # conn = DbConnection.dbconn(self="")
            # c = conn.cursor()
            # sql = 'select * from OSSRPT.API_AUTH where USERNAME= :uname'
            # c.execute(sql, uname=self.username)
            # row = c.fetchone()
            # print(row[0])

            if self.username == 'clarity':
                if hashpwd.hexdigest() == '518f8a60369d3a0b78b22b88af75b2a6':
                    # token = jwt.encode({'user': self.username, "iat": datetime.datetime.utcnow(),
                    #                     "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=600), },
                    #                    const.SECRET_KEY, algorithm="HS256")
                    # print(token)
                    # return {'success': 'true', 'token': token}
                    return 'success'

                # return make_response({'success': 'false', 'message': 'Invalid Credentials'}, 401,
                #                      {'WWW-Authenticate': 'Basic realm="Login required!"'})
                return 'Invalid Credentials'
            return 'Invalid Credentials'
        except TypeError:
            # return make_response({'success': 'false', 'message': 'Unauthorized User'}, 401,
            #                      {'WWW-Authenticate': 'Basic realm="Login required!"'})
            return 'Unauthorized User'
