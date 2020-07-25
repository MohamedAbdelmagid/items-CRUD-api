import sqlite3

from flask_restful import Resource, reqparse
from flask_jwt import jwt_required


class Item(Resource):
	
	TABLE_NAME = 'items'

	parser = reqparse.RequestParser()
	parser.add_argument(
		'price',
		type=float,
		required=True,
		help='This field cannot be left blank!'
	)

	@classmethod
	def find_by_name(cls, name):
		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()
		
		query = "SELECT * FROM {table} WHERE name=?".format(table=cls.TABLE_NAME)
		reslult = cursor.execute(query, (name,))
		row = reslult.fetchone()
		connection.close()

		if row:
			return {'item': {'name': row[0], 'price': row[1]}}

	@classmethod
	def insert(cls, item):
			connection = sqlite3.connect('data.db')
			cursor = connection.cursor()

			query = "INSERT INTO {table} VALUES(?, ?)".format(table=cls.TABLE_NAME)
			cursor.execute(query, (item['name'], item['price']))

			connection.commit()
			connection.close()

	@classmethod
	def update(cls, item):
		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()

		query = "UPDATE {table} SET price=? WHERE name=?".format(table=cls.TABLE_NAME)
		cursor.execute(query, (item['price'], item['name']))

		connection.commit()
		connection.close()

	def get(self, name):
		item = self.find_by_name(name)
		if item:
			return item
		return { 'message': 'item not found' }, 404

	def post(self, name):
		if self.find_by_name(name):
			return { 'message': "An item with name '{}' already exists.".format(name) }, 400
		
		data = Item.parser.parse_args()
		item = { 'name': name, 'price': data['price'] }
		try:
			self.insert(item)
		except:
			return { 'message': 'An error occured inserting the item.' }, 500

		return item, 201

	@jwt_required()
	def delete(self, name):
		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()

		query = "DELETE FROM {table} WHERE name=?".format(table=self.TABLE_NAME)
		cursor.execute(query, (name,))

		connection.commit()
		connection.close()

		return {'message': 'Item deleted'}
		
	@jwt_required()
	def put(self, name):
		data = Item.parser.parse_args()
		
		item = self.find_by_name(name)
		updated_item = { 'name': name, 'price': data['price'] }
		if item is None:	
			try:
				self.insert(updated_item)
			except:
				return {'message': 'An error occurred inserting the item.'}, 500
		else:
			try:
				self.update(updated_item)
			except:
				return {'message': 'An error occurred updating the item.'}, 500

		return updated_item, 201

class Items(Resource):
	TABLE_NAME = 'items'
	
	def get(self):
		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()

		query = "SELECT * FROM {table}".format(table=self.TABLE_NAME)
		result = cursor.execute(query)
		items = []
		for row in result:
				items.append({'name': row[0], 'price': row[1]})
		connection.close()

		return {'items': items}
			
