import sqlite3

from flask_restful import Resource, reqparse
from flask_jwt import jwt_required


class Item(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument(
		'price',
		type=float,
		required=True,
		help='This field cannot be left blank!'
	)

	def get(self, name):
		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()

		query = "SELECT * FROM items WHERE name=?"
		reslult = cursor.execute(query, (name,))
		row = reslult.fetchone()
		connection.close()

		if row:
			return {'item': {'name': row[0], 'price': row[1]}}
		return { 'message': 'item not found' }, 404

	def post(self, name):
		if next(filter(lambda item: item['name'] == name, items), None):
			return {'message': "An item with this name '{}' already exist".format(name)}, 400
		
		data = Item.parser.parse_args()
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
		data = Item.parser.parse_args()
		
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
