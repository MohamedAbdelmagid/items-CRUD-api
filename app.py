from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

items = [
	{ 'name': "chair", 'price': 12.30 },
	{ 'name': "door", 'price': 20.30 },
	{ 'name': "car", 'price': 16.30 },
]

class Item(Resource):

	def get(self, name):
		for item in items:
			if item['name'] == name:
				return item
		return { 'item': None }, 404

	def post(self, name):
		data = request.get_json()
		item = { 'name': name, 'price': data['price'] }
		items.append(item)
		return item, 201

class Items(Resource):
	def get(self):
		return { 'items': items }


api.add_resource(Item, '/item/<string:name>')
api.add_resource(Items, '/items')

app.run(port=5000, debug=True)