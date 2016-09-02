from .          import Data
from ..database import Database

class BlogData(Data):
	def __init__(self):
		Data.__init__(self)

	def get_active(self):
		db = Database.get_db()
		return db.blog_list.find({"is_active":True})