from datetime import timedelta

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, Items

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'super-secret'

app.config['JWT_EXPIRATION_DELTA'] = timedelta(hours=2)
app.config['JWT_AUTH_URL_RULE'] = '/login'

api = Api(app)
jwt = JWT(app, authenticate, identity)

@jwt.auth_response_handler
def customized_response_handler(access_token, identity):
	return {
		'access_token': access_token.decode('utf-8'),
		'user_id': identity.id
	}


api.add_resource(Item, '/item/<string:name>')
api.add_resource(Items, '/items')
api.add_resource(UserRegister, '/register')


if __name__ == "__main__":
	app.run()