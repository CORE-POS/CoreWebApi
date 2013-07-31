import os, os.path
import hashlib
from CoreWebApi import app
from flask import send_from_directory, abort
from werkzeug import secure_filename

class upload:

	def __init__(self):
		self.upload_dir = os.path.join(app.static_folder,'uploads')
		if not(os.path.isdir(self.upload_dir)):
			os.mkdir(self.upload_dir)

	def get_file(self, filename):
		filename = secure_filename(filename)	
		if os.path.isfile(os.path.join(self.upload_dir, filename)):
			return send_from_directory(self.upload_dir, filename)
		else:
			abort(404)

	def set_hash(self,filename):
		filename = secure_filename(filename)
		the_file = os.path.join(self.upload_dir,filename)
		the_hash = os.path.join(self.upload_dir,filename+".md5")
		if os.path.isfile(the_file):
			hash = hashlib.md5()
			with open(the_file, 'rb') as fp:
				chunk = 65536
				buf = fp.read(chunk)
				while len(buf) > 0:
					hash.update(buf)
					buf = fp.read(chunk)
				fp.close()

			file_hash = hash.hexdigest()
			with open(the_hash, 'w') as fp:
				fp.write(file_hash)
				fp.close()

	def get_hash(self,filename):
		filename = secure_filename(filename)
		the_file = os.path.join(self.upload_dir,filename)
		the_hash = os.path.join(self.upload_dir,filename+".md5")
		if os.path.isfile(the_file) and os.path.isfile(the_hash):
			with open(the_hash, 'r') as f:
				return f.read()
		elif os.path.isfile(the_file):
			self.set_hash(filename)
			if os.path.isfile(the_hash):
				with open(the_hash, 'r') as f:
					return f.read()
		return None

	def save(self, handle):
		filename = secure_filename(handle.filename)
		handle.save(os.path.join(self.upload_dir, filename))
		self.set_hash(filename)
		
