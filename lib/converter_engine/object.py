from pymongo          import MongoClient
from ..config.factory import ConfigFactory
import arrow

class ConverterConfig(object):
	def __init__(self):
		self.config = ConfigFactory.get(ConfigFactory.CONVERTER)
		self.config = self.config.get("converter")["target"]

	@property
	def target_connection_string(self):
		assert "ip" in self.config, "ip is not defined."
		if "username" in self.config and "password" in self.config and "authenticationDatabase" in self.config:
			connection_string = "mongodb://{username}:{password}@{ip}/test?authSource={authenticationDatabase}"
			connection_string = connection_string.format(
									              username = self.config["username"],
									              password = self.config["password"],
									                    ip = self.config["ip"],
									authenticationDatabase = self.config["authenticationDatabase"]
								)
		else:
			connection_string = "mongodb://{ip}:27017/test"
			connection_string = connection_string.format(ip=self.config["ip"])
		return connection_string	
	
class MentionDB(object):
	def __init__(self):
		self.config  = ConverterConfig()
		self.db      = MongoClient(self.config.target_connection_string)
		self.db      = self.db.isid
		self.mention = None

	def save(self):
		assert self.db      is not None, "db is not defined."
		assert self.mention is not None, "mention is not defined."

		self.db.mention.insert_one(self.mention)

	def set_as_converted(self, source_db=None):
		assert self.mention is not None, "mention is not defined."
		assert source_db    is not None, "source_db is not defined."

		source_db.data.update(
			{"permalink":self.mention["MentionDirectLink"]},
			{"$set":{"converted":True}}
		)

class AuthorInfoDB(object):
	def __init__(self):
		self.config      = ConverterConfig()
		self.db          = MongoClient(self.config.target_connection_string)
		self.db          = self.db.isid
		self.author_info = None

	def generate_info(self, mention=None):
		assert "SourceName"        in mention, "SourceName is not defined."
		assert "AuthorId"          in mention, "AuthorId is not defined."
		assert "AuthorName"        in mention, "AuthorName is not defined."
		assert "AuthorDisplayName" in mention, "AuthorDisplayName is not defined."
		assert "AuthorLocation"    in mention, "AuthorLocation is not defined."

		update_time      = arrow.utcnow().to("Asia/Singapore").format("YYYY-MM-DD HH:mm:ss")
		update_time_iso  = arrow.utcnow().format("YYYY-MM-DD HH:mm:ss")
		self.author_info = {
			                "AuthorType" : mention["SourceName"],
			                  "AuthorId" : mention["AuthorId"],
			          "AuthorScreenName" : mention["AuthorName"],
			         "AuthorDisplayName" : mention["AuthorDisplayName"],
			            "AuthorLocation" : mention["AuthorLocation"],
			       "AuthorFollowerCount" : -1,
			         "AuthorFriendCount" : -1,
			         "AuthorStatusCount" : -1,
			            "AuthorLanguage" : "",
			"AuthorTotalMentionsCrawled" : 1,
			           "LastUpdatedDate" : update_time,
			        "LastUpdatedDateISO" : update_time_iso.replace(" ","T") + "Z"
		}

	def save(self):
		assert self.author_info is not None, "author_info is not None."

		documents    = self.db.author_info.find({
							"AuthorScreenName" : self.author_info["AuthorScreenName"],
							      "AuthorType" : self.author_info["AuthorType"]
					   })
		documents    = [document for document in documents]
		is_duplicate = True if len(documents) > 0 else False

		if is_duplicate:
			self.db.author_info.update_one(
				{
				  	"AuthorScreenName":self.author_info["AuthorScreenName"],
					      "AuthorType":self.author_info["AuthorType"]
				},
				{
					"$inc":{"AuthorTotalMentionsCrawled":1},
					"$set":{
						   "LastUpdatedDate":self.author_info["LastUpdatedDate"], 
						"LastUpdatedDateISO":self.author_info["LastUpdatedDateISO"]
					}
				}
			)
		else:
			self.db.author_info.insert_one(self.author_info)