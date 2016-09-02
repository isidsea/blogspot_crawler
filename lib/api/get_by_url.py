from .              	 import API, Key
from ..exceptions   	 import CannotFindBlog, APIKeyLimitExceed, EmptyPost, APIBackendError
from ..validator.factory import ValidatorFactory
import requests
import copy

class GetByURLAPI(API):
	def __init__(self):
		API.__init__(self, end_point="https://www.googleapis.com/blogger/v3/blogs/byurl")

	def execute(self, url=None):
		API.execute(self)
		
		assert url is not None, "url is not defined."

		try_again = True
		while try_again:
			try:
				key = Key.get_key()
				res = requests.get("%s?url=%s&key=%s" % (self.end_point, url, Key.get_key()))
				res = res.json()

				response_validator = ValidatorFactory.get_validator(ValidatorFactory.RESPONSE)
				response_validator.validate(res)

				if "id" not in res:
					raise CannotFindBlog("Cannot find %s's ID" % url)
				try_again = False # Set try_again == False when everything is good
			except APIKeyLimitExceed:
				pass
			except APIBackendError:
				pass
			except EmptyPost:
				try_again = False
		return copy.deepcopy(res)