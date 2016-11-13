from ..database   import Database
from curtsies     import fmtstr
import copy

class KeyManager:
	def __init__(self, **kwargs):
		self.holder        = kwargs.get("holder", None)
		self.current_index = kwargs.get("current_index", 0)
		self.keys          = kwargs.get("keys", self.get_keys())
		self.selected_key  = kwargs.get("selected_key", self.get_key())

	def get_keys(self):
		dbObject = Database()

		db   = dbObject.get_db()
		keys = db.api_keys.find({"is_active":True})

		if keys is not None:
			keys = [key["key"] for key in keys]
		dbObject.close()
		return keys

	def get_key(self):
		assert self.holder    is not None, "holder is not defined."
		assert len(self.keys) > 0        , "No API Key in the list."

		self.selected_key = copy.copy(self.keys[self.current_index])
		is_available      = self.check_availability(self.selected_key)
		if not is_available:
			self.selected_key = self.next_key()
		self.mark_key()
		return self.selected_key

	def next_key(self):
		self.next_index()
		return self.get_key()

	def next_index(self):
		self.current_index += 1
		if self.current_index >= len(self.keys):
			self.current_index = 0

	def check_availability(self, key=None):
		assert self.holder is not None, "holder is not defined."
		assert key         is not None, "key is not defined."

		dbObject = Database()

		db     = dbObject.get_db()
		worker = db.workers.find_one({"$and":[{"current_key": key}, {"name": {"$ne":self.holder}}]})
		dbObject.close()

		if worker is not None:
			return False
		return True

	def mark_key(self):
		assert self.holder       is not None, "holder is not defined."
		assert self.selected_key is not None, "key is not defined."

		dbObject = Database()

		db = dbObject.get_db()
		db.workers.create_index("name", unique=True, background=True)
		
		# Check if worker is exist or not
		worker = db.workers.find_one({"name": self.holder})
		if worker is None:
			document = {
				"name": self.holder,
				"current_key": self.selected_key
			}
			db.workers.insert_one(document)
		else:
			db.workers.update({"name": self.holder},{"$set":{"current_key": self.selected_key}})
		dbObject.close()

	def count_as_used(self):
		dbObject = Database()

		db = dbObject.get_db()
		db.api_keys.update({"key": self.selected_key},{"$inc":{"used": 1}})
		dbObject.close()