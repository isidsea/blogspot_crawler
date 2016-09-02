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
					# print(bson.json_util.dumps(res,indent=4))

					for item in res["items"]:
						content  = BeautifulSoup(item["content"], "html5lib")
						content  = content.text
						document = {
							   "_insert_time" : arrow.utcnow().datetime,
							       "_country" : blog["country"],
							        "_origin" : blog["domain"],
							"pubslished_date" : arrow.get(item["published"]).datetime,
							      "permalink" : item["url"],
							          "title" : item["title"],
							        "content" : content,
							      "author_id" : item["author"]["id"],
							    "author_name" : item["author"]["displayName"]
						}
						callback(document=document)
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
		except pymongo.errors.DuplicateKeyError:
			print(fmtstr("[post_list_api][error] Duplicate document!","red"))
		except EmptyPost as ex:
			print(fmtstr("[post_list_api][error] %s" % ex, "red"))