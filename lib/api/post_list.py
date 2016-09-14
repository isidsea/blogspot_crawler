from .        			 import API, Key
from ..validator.factory import ValidatorFactory
from ..exceptions        import APIBackendError, APIKeyLimitExceed, EmptyPost
from bs4      			 import BeautifulSoup
from curtsies 			 import fmtstr
import pymongo
import requests
import arrow
import copy
import bson.json_util

class PostListAPI(API):
	def __init__(self):
		API.__init__(self, end_point="https://www.googleapis.com/blogger/v3/blogs/%s/posts?maxResult=500&key=%s")

	def execute(self, args=None, blog=None, callback=None):
		try:
			API.execute(self)

			if args is not None:
				blog, callback = args
			assert blog     is not None, "blog is not defined."
			assert "id"     in blog    , "id is not defined."
			assert callback is not None, "callback is not defined."

			print("[post_list_api][debug] Crawling: %s" % blog["id"])
			# Crawling posts
			has_next 	= True
			current_url = copy.copy(self.end_point)
			while has_next:
				try:
					url = current_url % (blog["id"], Key.get_key())
					res = requests.get(url)
					res = res.json()

					response_validator = ValidatorFactory.get_validator(ValidatorFactory.RESPONSE)
					response_validator.validate(res)

					for item in res["items"]:
						callback(document=self.generate_document(blog,item))
					# You need to make sure that the next request is not retrying current request.
					# If you need to retry, please do not go to next page
					has_next = "nextPageToken" in res
					if has_next:
						# url = self.end_point % (blog["id"],Key.get_key())
						token_url = "&pageToken=%s" % res["nextPageToken"]
						current_url = "%s%s" % (current_url, token_url)
						print("[post_list_api][debug] Going to %s next page items" % blog["id"])
				except APIBackendError as ex:
					print(fmtstr("[post_list_api][error] %s" % ex, "red"))
				except APIKeyLimitExceed as ex:
					print(fmtstr("[post_list_api][error] %s" % ex, "red"))
				except CannotFindBlog as ex:
					print(fmtstr("[post_list_api][error] %s" % ex, "red"))
		except pymongo.errors.DuplicateKeyError:
			print(fmtstr("[post_list_api][error] Duplicate document!","red"))
		except EmptyPost as ex:
			print(fmtstr("[post_list_api][error] %s" % ex, "red"))

	def generate_document(self, blog=None, item=None):
		content  = BeautifulSoup(item["content"], "html5lib")
		content  = content.text
		document = {}
		document.update({"_insert_time":arrow.utcnow().datetime})
		document.update({"_country":blog["country"]})
		document.update({"origin":blog["domain"]})
		document.update({"published_date":arrow.get(item["published"]).datetime})
		document.update({"permalink":item["url"]})
		document.update({"title":item["title"]})
		document.update({"content":content})
		document.update({"author_id":item["author"]["id"]})
		document.update({"author_name":item["author"]["displayName"]})
		document.update({"converted":False})
		return document