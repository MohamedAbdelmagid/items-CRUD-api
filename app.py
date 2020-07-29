import os
from datetime import timedelta

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, Items
from resources.store import Store, Stores
from database import db

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'super-secret'

app.config['JWT_EXPIRATION_DELTA'] = timedelta(hours=2)
app.config['JWT_AUTH_URL_RULE'] = '/login'
app.config['PROPAGATE_EXCEPTIONS'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

api = Api(app)
jwt = JWT(app, authenticate, identity)

@jwt.auth_response_handler
def customized_response_handler(access_token, identity):
	return {
		'access_token': access_token.decode('utf-8'),
		'user_id': identity.id
	}

@app.before_first_request
def create_tables():
	db.create_all()

api.add_resource(Item, '/item/<string:name>')
api.add_resource(Items, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(Stores, '/stores')


if __name__ == "__main__":
	app.run()