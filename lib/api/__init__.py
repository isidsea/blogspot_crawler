from ..database   import Database
import requests
import random
import os

class API:
	def __init__(self, **kwargs):
		self.end_point = kwargs.get("end_point", None)

	def execute(self, **kwargs):
		assert self.end_point is not None, "end_point is not defined."

# class Key:
# 	def __init__(self):
# 		pass

# 	@classmethod
# 	def get_keys(self):
# 		# Get API Key from Database
# 		dbObject = Database()

# 		db   = dbObject.get_db()
# 		keys = db.api_keys.find({"$and":[{"is_active":True}]})

# 		if keys is not None:
# 			for key in keys:
# 				yield key["key"]
# 		dbObject.close()

# 	@classmethod  
# 	def check_availability(self, holder=None, key=None):
# 		assert key    is not None, "key is not defined."
# 		assert holder is not None, "holder is not defined."

# 		dbObject = Database()

# 		db     = dbObject.get_db()
# 		worker = db.workers.find_one({"$and":[{"current_key": key}, {"name": {"$ne":holder}}]})
# 		dbObject.close()

# 		if worker is not None:
# 			raise KeyIsUsed("Key is used by %s" % worker["name"])

# 	@classmethod
# 	def mark_it(self, holder=None, key=None):
# 		assert holder is not None, "holder is not defined."
# 		assert key    is not None, "key is not defined."

# 		dbObject = Database()

# 		db = dbObject.get_db()
# 		db.workers.create_index("name", unique=True, background=True)
# 		db.workers.create_index("current_key", unique=True, background=True)
		
# 		# Check if worker is exist or not
# 		worker = db.workers.find_one({"name": holder})
# 		if worker is None:
# 			document = {
# 				"name": holder,
# 				"current_key": key
# 			}
# 			db.workers.insert_one(document)
# 		else:
# 			db.workers.update({"name": holder},{"$set":{"current_key": key}})
# 		dbObject.close()
