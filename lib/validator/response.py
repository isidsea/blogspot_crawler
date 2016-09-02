from . import Validator
from ..exceptions import CannotFindBlog, APIBackendError, APIKeyLimitExceed, EmptyPost

class ResponseValidator(Validator):
	def __init__(self):
		Validator.__init__(self)

	def validate(self, response=None):
		Validator.validate(self, response)

		if "error" in response:
			if response["error"]["code"] == 404: raise CannotFindBlog("Cannot find the blog inside blogspot")
			if response["error"]["code"] == 503: raise APIBackendError("Google Blogspot API Backend error 503")
			if response["error"]["code"] == 403: raise APIKeyLimitExceed("Running out of request limit.")
			raise CannotFindBlog("Cannot find the blog inside blogspot with error: %s" % res["code"])
		elif "items" not in response:
			raise EmptyPost("Blog does not have any post.")