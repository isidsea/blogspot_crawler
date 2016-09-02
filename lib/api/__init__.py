import requests
import random
import os

class API:
	def __init__(self, **kwargs):
		self.end_point = kwargs.get("end_point", None)

	def execute(self, **kwargs):
		assert self.end_point is not None, "end_point is not defined."

class Key:
	def __init__(self):
		pass

	@classmethod
	def get_key(self):
		key_path     = os.path.join(os.getcwd(), "data", "api_keys.txt")
		file         = open(key_path,"r")
		keys         = [line.replace("\n","") for line in file.readlines()]
		selected_key = random.sample(keys,1)[0]
		return selected_key
		