from .object    import MentionDB, AuthorInfoDB
from .engine    import Engine as ConverterEngine
from ..database import Database
from ..data     import Data
from curtsies   import fmtstr
import pymongo

class ConverterInterface:
	def __init__(self):
		pass

	@classmethod
	def multiple_convert_and_save(self):
		documents      = Data.get_not_converted()
		mention_db     = MentionDB()
		author_info_db = AuthorInfoDB()
		for document in documents:
			try:
				converted_document = ConverterEngine.convert(document).to_dict()

				mention_db.mention = converted_document
				mention_db.save()

				author_info_db.generate_info(converted_document)
				author_info_db.save()
			except pymongo.errors.DuplicateKeyError:
				print(fmtstr("[convert][error] Duplicate Document!","red"))
			finally:
				mention_db.set_as_converted(source_db=Database.get_db())