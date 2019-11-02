import os

def create_dir_if_not_exists(dir_path):
	"""
	Create the given directory if it doesn't already exist

	Parameters:
		dir_path (str): directory to create if not exists
	"""
	if not os.path.exists(dir_path):
		os.makedirs(dir_path)