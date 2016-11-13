from .          import Data
from ..database import Database

class BlogData(Data):
	def __init__(self):
		Data.__init__(self)

	def get_active(self):

		dbObject = Database()
		db    	 = dbObject.get_db()
		blogs 	 = db.blog_list.find({"is_active":True})
		dbObject.close()

		return blogs