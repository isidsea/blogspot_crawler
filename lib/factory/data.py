from ..data.blog import BlogData
from ..data.post import PostData

class DataFactory:
	BLOG = 0
	POST = 1

	def __init__(self):
		pass

	@classmethod
	def get_data(self, data_name=None):
		assert data_name is not None, "data_name is not defined."

		if data_name == DataFactory.BLOG:
			return BlogData()
		elif data_name == DataFactory.POST:
			return PostData()