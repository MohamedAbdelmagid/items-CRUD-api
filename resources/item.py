from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.item import ItemModel


class Item(Resource):

	parser = reqparse.RequestParser()
	parser.add_argument(
		'price',
		type=float,
		required=True,
		help='This field cannot be left blank!'
	)

	def get(self, name):
		item = ItemModel.find_by_name(name)
		if item:
			return item.json()
		return { 'message': 'item not found' }, 404

	def post(self, name):
		if ItemModel.find_by_name(name):
			return { 'message': "An item with name '{}' already exists.".format(name) }, 400
		
		data = Item.parser.parse_args()
		item = ItemModel(name, data['price'])
		try:
			item.save_in_database()
		except:
			return { 'message': 'An error occured inserting the item.' }, 500

		return item.json(), 201

	@jwt_required()
	def delete(self, name):
		item = ItemModel.find_by_name(name)
		if item:
			item.delete_from_database()

		return {'message': 'Item deleted'}, 201
		
	@jwt_required()
	def put(self, name):
		data = Item.parser.parse_args()
		
		item = ItemModel.find_by_name(name)
		if item is None:
			item = ItemModel(name, data['price'])
		else:
			item.price = data['price']

		item.save_in_database()

		return updated_item.json(), 201

class Items(Resource):
	
	def get(self):
		return {'items': [item.json() for item in ItemModel.query.all()]}
			
