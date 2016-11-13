import pymongo

class Database:
	def __init__(self, **kwargs):
		self.conn = None
		self.db   = None

		self.host = kwargs.get("host","mongo")
		self.name = kwargs.get("name","blogspot_crawler")

	def get_db(self):
		self.conn = pymongo.MongoClient("mongodb://%s:27017" % (self.host))
		self.db   = conn[self.name]

		self.db.blog_list.create_index([("id", pymongo.ASCENDING)], unique=True, background=True)
		self.db.data.create_index([("permalink", pymongo.ASCENDING)], unique=True, background=True)
		return self.db

	def close(self):
		if self.conn is not None:
			self.conn.close()