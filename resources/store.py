from flask_restful import Resource
from flask_jwt import jwt_required

from models.store import StoreModel

class Store(Resource):

	def get(self, name):
		store = StoreModel.find_by_name(name)
		if not store:
			return {'message': 'Store not found'}, 404

		return store.json()
		
	#	Add new store to the database if not already exists
	@jwt_required()
	def post(self, name):
		if StoreModel.find_by_name(name):
			return {'message': "A store with name '{}' already exists.".format(name)}, 400
		
		store = StoreModel(name)
		try:
			store.save_in_database()
		except:
			return {'message': 'An error occurred while creating the store.'}, 500

		return store.json(), 201
		
	# Delete a store from the database
	@jwt_required()		
	def delete(self, name):
		store = StoreModel.find_by_name(name)
		if not store:
			return {'message': 'Store is already deleted or not exists!'}, 204

		store.delete_from_database()
		
		return {'message': 'Store deleted!'}, 200


class Stores(Resource):
	
	def get(self):
		return { 'stores': [store.json() for store in StoreModel.find_all()]}