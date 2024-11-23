from flask import Flask, request, jsonify, make_response
from functools import wraps
from werkzeug.security import check_password_hash, generate_password_hash
from flask_restful import Resource, Api
from cryptography.hazmat.primitives.serialization import pkcs12
from cryptography.hazmat.primitives import serialization
from logging.handlers import RotatingFileHandler
import requests
import simplejson as json
import logging
import jwt
import datetime
import os
import traceback
import cx_Oracle
import hashlib

app = Flask(__name__)
api = Api(app)

app.config['SECRET_KEY'] = '!2PyTHon23Fla63$sk!34api90&&'


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message': 'Token is missing!'})

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            print(data)
        except:
            return {'message': 'Token is invalid!'}, 401

        return f(*args, **kwargs)

    return decorated


def getLogger(logname, logdir, logsize=2000 * 1024, logbackup_count=10):
    if not os.path.exists(logdir):
        os.makedirs(logdir)
    logfile = '%s/%s.log' % (logdir, logname)
    loglevel = logging.INFO
    logger = logging.getLogger(logname)
    logger.setLevel(loglevel)
    if logger.handlers is not None and len(logger.handlers) >= 0:
        for handler in logger.handlers:
            logger.removeHandler(handler)
        logger.handlers = []
    loghandler = logging.handlers.RotatingFileHandler(
        logfile, maxBytes=logsize, backupCount=logbackup_count)
    formatter = logging.Formatter('%(asctime)s-%(levelname)s-%(message)s')

    loghandler.setFormatter(formatter)
    logger.addHandler(loghandler)
    return logger


logger = getLogger('kasperskyapi', 'logs')

with open("Kaspersky/386abd33d873403ebfd353f6f6a723c3626963f583c04f85b0e8f362d45be174.pfx", "rb") as f:
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

headers = {
    'Content-type': 'application/json',
    'Accept': 'application/json'}

cert = ("cert.pem", "key.pem")


class login(Resource):

    def post(self):
        auth = request.authorization

        if not auth or not auth.username or not auth.password:
            return make_response({'message': 'Authentication Required'}, 401,
                                 {'WWW-Authenticate': 'Basic realm="Login required!"'})

        hashpwd = hashlib.md5(auth.password.encode())

        dsn_tns = cx_Oracle.makedsn('172.25.1.172', '1521', service_name='clty')
        conn = cx_Oracle.connect(user='SLT012583', password='!23qweASD', dsn=dsn_tns)
        c = conn.cursor()
        sql = 'select * from SLT012583.API_AUTH where USERNAME= :uname'
        c.execute(sql, uname=auth.username)
        row = c.fetchone()

        if not row[0]:
            return make_response({'message': 'Unauthorized User'}, 401,
                                 {'WWW-Authenticate': 'Basic realm="Login required!"'})

        elif hashpwd.hexdigest() == row[1]:
            token = jwt.encode({'user': auth.username, "iat": datetime.datetime.utcnow(),
                                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=1), },
                               app.config['SECRET_KEY'], algorithm="HS256")
            print(token)
            return {'token': token}

        return make_response({'message': 'Invalid Credentials'}, 401,
                             {'WWW-Authenticate': 'Basic realm="Login required!"'})


class createsub(Resource):
    @token_required
    def post(self):
        data = request.get_json()
        logger.info("Request : %s" % data)
        # subid= data['Customer']
        # con =subid['Contacts']
        # conname = con['CompanyName']

        createresponse = requests.post('https://api.demo.korm.kaspersky.com/Subscriptions/v2.0/api/Subscription/create',
                                       cert=cert,
                                       data=json.dumps(data),
                                       headers=headers)

        resmsg = json.loads(createresponse.text)
        responsedata = {"message": resmsg['Message']}
        logger.info("Response : %s" % responsedata)
        return responsedata, 201


class modifysub(Resource):
    @token_required
    def post(self):
        data = request.get_json()
        logger.info("Request : %s" % data)
        createresponse = requests.post(
            'https://api.demo.korm.kaspersky.com/Subscriptions/v2.0/api/Subscription/modifyexpiration',
            cert=cert,
            data=json.dumps(data),
            headers=headers)

        resmsg = json.loads(createresponse.text)
        responsedata = {"message": resmsg['Message']}
        logger.info("Response : %s" % responsedata)
        return responsedata


class removesub(Resource):
    @token_required
    def post(self):
        data = request.get_json()
        # app.logger.info("Request :" +str(data))
        logger.info("Request : %s" % data)

        createresponse = requests.post(
            'https://api.demo.korm.kaspersky.com/Subscriptions/v2.0/api/Subscription/hardcancel',
            cert=cert,
            data=json.dumps(data),
            headers=headers)

        resmsg = json.loads(createresponse.text)
        responsedata = {"message": resmsg['Message']}
        logger.info("Response : %s" % responsedata)
        return responsedata


api.add_resource(login, '/api/kasperskey/login/')
api.add_resource(createsub, '/api/kasperskey/createsub/')
api.add_resource(modifysub, '/api/kasperskey/modifysub/')
api.add_resource(removesub, '/api/kasperskey/removesub/')

if __name__ == '__main__':
    app.run(debug=True, port=5002)
