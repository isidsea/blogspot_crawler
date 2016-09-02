from pymongo          import MongoClient
from .template        import MentionTemplate
import arrow
import hashlib

class Engine(object):

	def __init__(self):
		pass
		# self.config_file = ConfigFactory.get(ConfigFactory.CONVERTER)

	@classmethod
	def convert(self, document=None):
		assert document is not None, "document is not defined."

		new_document                              = MentionTemplate()
		new_document.MentionId                    = hashlib.sha256(document["permalink"].encode("utf-8")).hexdigest() 
		new_document.MentionText                  = document["content"]
		new_document.MentionMiscInfo			  = ""
		new_document.MentionType                  = document["origin"] 
		new_document.MentionDirectLink            = document["permalink"]
		new_document.MentionCreatedDate           = document["published_date"]
		new_document.MentionCreatedDateISO        = document["published_date"]
		new_document.AuthorId                     = document["author_id"] if "author_id" in document else document["author_name"]
		new_document.AuthorName                   = document["author_name"]
		new_document.AuthorDisplayName            = document["author_name"]
		new_document.SourceType                   = "Blogs"
		new_document.SourceName                   = document["origin"] 
		new_document.SentFromHost                 = "220.100.163.132"
		new_document.DateInsertedIntoCrawlerDB    = document["_insert_time"]
		new_document.DateInsertedIntoCrawlerDBISO = document["_insert_time"]
		new_document.DateInsertedIntoCentralDB    = arrow.utcnow().datetime
		new_document.DateInsertedIntoCentralDBISO = arrow.utcnow().datetime
		new_document.Country                      = document["_country"]
		return new_document