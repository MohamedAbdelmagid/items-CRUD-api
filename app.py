from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate, identity

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'super-secret'

api = Api(app)
jwt = JWT(app, authenticate, identity)

items = [
	{ 'name': "chair", 'price': 12.30 },
	{ 'name': "door", 'price': 20.30 },
	{ 'name': "car", 'price': 16.30 },
]

class Item(Resource):
	def get(self, name):
		item = next(filter(lambda item: item['name'] == name, items), None)
		return { 'item': item }, 200 if item else 404

	def post(self, name):
		if next(filter(lambda item: item['name'] == name, items), None):
			return {'message': "An item with this name '{}' already exist".format(name)}, 400
			
		data = request.get_json()
		item = { 'name': name, 'price': data['price'] }
		items.append(item)
		return item, 201

	@jwt_required()
	def delete(self, name):
		global items
		items = list(filter(lambda item: item['name'] != name, items))
		return { 'message': 'Item deleted' }
		
	@jwt_required()
	def put(self, name):
		parser = reqparse.RequestParser()
		parser.add_argument(
			'price',
			type=float,
			required=True,
			help='This field cannot be left blank!'
		)
		data = parser.parse_args()
		
		item = next(filter(lambda item: item['name'] == name, items), None)
		if item is None:	
			item = { 'name': name, 'price': data['price'] }
			items.append(item)
		else:
			item.update(data)

		return item, 201

class Items(Resource):
	def get(self):
		return { 'items': items }


api.add_resource(Item, '/item/<string:name>')
api.add_resource(Items, '/items')

app.run()