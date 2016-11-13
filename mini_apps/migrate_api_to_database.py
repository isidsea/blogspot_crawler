import os
import sys

TEST_DIR   = os.path.abspath(os.path.dirname(__file__))
PARENT_DIR = os.path.join(TEST_DIR, '..')
sys.path.insert(0, PARENT_DIR)

import pymongo

if __name__ == "__main__":
	key_path = os.path.join(os.getcwd(), "data","api_keys.txt")
	key_file = open(key_path, "r")
	keys     = [key.replace("\n","") for key in key_file.readlines()]
	
	for key in keys:	
		conn = pymongo.MongoClient("mongodb://mongo/blogspot_crawler")
		db   = conn["blogspot_crawler"]

		document = {
			"key": key,
			"used": 0,
			"is_active": True
		}
		
		db.api_keys.create_index("key",unique=True, background=True)
		db.api_keys.create_index("is_active", background=True)
		db.api_keys.insert_one(document)
		conn.close()
