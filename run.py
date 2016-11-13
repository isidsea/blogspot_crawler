from lib.factory.data import DataFactory
from lib.factory.api  import APIFactory
from lib.database     import Database
from multiprocessing  import Pool

if __name__ == "__main__":
	blog_data = DataFactory.get_data(DataFactory.BLOG)
	post_data = DataFactory.get_data(DataFactory.POST)
	blogs     = blog_data.get_active()
	blogs     = [(blog, post_data.post_list_callback) for blog in blogs]

	with Pool(5) as pool:
		post_list = APIFactory.get_api(APIFactory.POST_LIST)
		pool.map(post_list.execute, blogs)