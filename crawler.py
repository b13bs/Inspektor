import os
import imghdr

_extension = '*'
_directory = '.'

def set_extension(ext):
	global _extension
	_extension = ext
def set_directory(dir):
	global _directory
	_directory = dir

#actually get the file paths (relative)
def all_files(dir):
	for path, dirs, files in os.walk(dir):
		for f in files:
			yield os.path.join(path, f)
			
#crawls from the given directory and filters out file extension if given
def get_files():
	if _extension != '*':
		return [f for f in all_files(_directory) if f.endswith('.' + _extension)]
	else:
		return [f for f in all_files(_directory)]
		
#get the file type 
#supported file types: https://docs.python.org/2/library/imghdr.html
def get_file_type(file):
	return imghdr.what(file)