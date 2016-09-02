import pymongo

class Database:
	def __init__(self):
		pass

	@classmethod
	def get_db(self):
		db = pymongo.MongoClient("mongodb://mongo:27017")
		db = db["blogspot_crawler"]

		db.blog_list.create_index([("id", pymongo.ASCENDING)], unique=True)
		db.data.create_index([("permalink", pymongo.ASCENDING)], unique=True)
		return db