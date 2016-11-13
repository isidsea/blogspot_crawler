from ..api.get_by_url import GetByURLAPI
from ..api.post_list  import PostListAPI

class APIFactory:
	GET_BY_URL = 0
	POST_LIST  = 1
	
	def __init__(self):
		pass

	@classmethod
	def get_api(self, api_name=None):
		assert api_name is not None, "api_name is not defined."

		if api_name == APIFactory.GET_BY_URL:
			return GetByURLAPI()
		elif api_name == APIFactory.POST_LIST:
			return PostListAPI()