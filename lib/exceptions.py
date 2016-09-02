class CannotFindField(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

class CannotFindFile(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

class CannotFindBlog(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

class APIKeyLimitExceed(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

class APIBackendError(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

class EmptyPost(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)