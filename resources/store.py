from flask_restful import Resource
from models.store import StoreModel

class Store(Resource):

	def get(self, name):
		store = StoreModel.find_by_name(name)
		if store:
			return store.json()
		return {'message': 'Store not found'}, 404
		
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
		if store:
			store.delete_from_database()
		else:
			return 204

		return {'message': 'Store deleted!'}, 200


class Stores(Resource):
	
	def get(self):
		return { 'stores': [store.json() for store in StoreModel.query.all()]}