from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.item import ItemModel
from models.store import StoreModel


class Item(Resource):

	parser = reqparse.RequestParser()
	parser.add_argument(
		'price',
		type=float,
		required=True,
		help='This field cannot be left blank!'
	)
	parser.add_argument(
		'store_id',
		type=int,
		required=True,
		help='Every item should have a store id!!'
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
		item = ItemModel(name, **data)
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

		return {'message': 'Item deleted'}, 200
		
	@jwt_required()
	def put(self, name):
		data = Item.parser.parse_args()

		#	Check if there is a store with this id
		if StoreModel.find_by_id(data['store_id']):
			#	Create a new item if it's not found
			item = ItemModel.find_by_name(name)
			if item:
				item.price = data['price']
				item.store_id = data['store_id']
			else:
				item = ItemModel(name, **data)

			item.save_in_database()
		else:
			return { 'message': "No store with id '{}' found!".format(data['store_id']) }, 400


		return item.json(), 201

class Items(Resource):
	
	def get(self):
		return {'items': [item.json() for item in ItemModel.find_all()]}
			
