""" This migration script will read every link provided inside data/blog_list.txt
	If you want to add new blog, you can modify that data/blog_list.txt
"""

from lib.exceptions    import CannotFindFile, CannotFindBlog, EmptyPost
from lib.network_tools import NetworkTools
from lib.database      import Database
from lib.api.factory   import APIFactory
from curtsies          import fmtstr
import os
import requests
import pymongo
import arrow

if __name__ == "__main__":
	file = os.path.join(os.getcwd(),"data","blog_list.csv")
	if not os.path.isfile(file): raise CannotFindFile("Cannot find %s file" % file)

	print("[migrate][debug] Migarting...")
	file = open(file,"r", encoding="utf-8")
	for line in file.readlines():
		try:
			line    = line.replace("\n","")
			line    = line.split(",")
			country = line[0]
			url     = line[2]
			url     = url.replace('"',"")
			url     = url.replace("'","")
			url     = url.replace(" ","")
			url     = url.replace("#","")
			url     = url.replace("-","")
			url     = NetworkTools.full_url(url)
			# basic_url = url.replace("\n","")

			print("[migrate][debug] URL: %s" % url.encode("utf8"))
			get_by_url = APIFactory.get_api(APIFactory.GET_BY_URL)
			res        = get_by_url.execute(url=url)

			if country is None: raise CannotFindBlog("Country is null")
			document = {
				          "id" : res["id"],
				        "name" : res["name"],
				 "description" : res["description"],
				     "created" : arrow.get(res["published"]).datetime,
				     "updated" : arrow.get(res["updated"]).datetime,
				         "url" : res["url"],
				      "domain" : NetworkTools.get_domain(res["url"], with_scheme=False),
				     "country" : country,
			    "_insert_time" : arrow.utcnow().datetime,
			       "is_active" : True
			}
			db = Database.get_db()
			db.blog_list.insert_one(document)
		except CannotFindBlog as ex:
			print(fmtstr("[migrate][debug] %s" % ex,"red"))
		except pymongo.errors.DuplicateKeyError:
			print(fmtstr("[migrate][debug] Blog has already exists.","red"))
	print("[migrate][debug] Migrated!")