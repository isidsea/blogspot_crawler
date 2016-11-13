from .   	    import Data
from ..database import Database
from curtsies   import fmtstr
import pymongo

class PostData(Data):
	def __init__(self):
		Data.__init__(self)

	def post_list_callback(self, document=None):
		assert document is not None, "document is not defined."
		dbObject = Database()

		db = dbObject.get_db()
		db.data.insert_one(document)

		dbObject.close()
		print("[post_list_callback][debug] Inserted one document!")

	def get_not_converted(self):
		db = Database.get_db()
		return [doc for doc in db.data.find({"$or":[{"converted":None},{"converted":False}]})]