import os
import sys

TEST_DIR   = os.path.abspath(os.path.dirname(__file__))
PARENT_DIR = os.path.join(TEST_DIR, '..')
sys.path.insert(0, PARENT_DIR)

from lib.manager.key import KeyManager

def test_get_keys():
	# Preparing Key List
	key_path = os.path.join(os.getcwd(), "data", "api_keys.txt")
	key_file = open(key_path, "r")
	keys     = [key.replace("\n","") for key in key_file.readlines()]

	key_manager = KeyManager()
	assert [key for key in key_manager.keys] == keys
