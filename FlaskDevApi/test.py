import resource as testing

from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager

from jwt import InvalidSignatureError


app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = 'secret-key'
app.config['JWT_HEADER_TYPE'] = 'AUTH_T'
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['DEBUG'] = False


api = Api(app)
jwt = JWTManager(app)


@jwt.invalid_token_loader
def invalid_token():
    return jsonify({
        'message': 'Invalid token.',
        'error': 'invalid_token'
    }), 401


@jwt.revoked_token_loader
def revoked_token():
    return jsonify({
        'message': 'Token is revoked.',
        'error': 'revoked_token'
    }), 401


@app.errorhandler(InvalidSignatureError)
def invalid_signature():
    return jsonify({
        'message': 'Invalid signature token.',
        'error': 'wrong_token'
    }), 401


api.add_resource(testing.Testing, '/test')


if __name__ == '__main__':
    app.run(port=5000, debug=False)