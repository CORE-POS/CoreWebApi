from flask import send_from_directory, request, redirect, url_for, abort
from CoreWebApi import app
from CoreWebApi.database import db_session
from CoreWebApi.models import ProductUser, Products
from CoreWebApi.json_out import json_as_configured
from CoreWebApi.uploads import upload
from sqlalchemy import or_

@app.route('/')
def index():
	return send_from_directory(app.static_folder,'api.html')

@app.route('/item/<upc>')
def show_item(upc):
	item=Products.query.get(upc.zfill(13))
	return json_as_configured(item.serialize())

@app.route('/sales/')
def get_sales():
	results = Products.query.join(Products.productUser)\
		.filter(Products.discounttype == 1)\
		.order_by(ProductUser.brand, Products.upc)
	return json_as_configured([i.serialize() for i in results])

@app.route('/membersales/')
def get_mem_sales():
	results = Products.query.join(Products.productUser)\
		.filter(Products.discounttype == 2)\
		.order_by(ProductUser.brand, Products.upc)
	return json_as_configured([i.serialize() for i in results])

@app.route('/search/<term>')
def search_results(term):
	results = Products.query.join(Products.productUser)\
		.filter(or_(
			Products.description.like('%'+term+'%'),
			ProductUser.description.like('%'+term+'%'),
			ProductUser.brand.like('%'+term+'%')\
		))\
		.order_by(Products.upc)
	return json_as_configured([i.serialize() for i in results])

@app.route('/file/', methods=['GET','POST'])
def upload_file():
	if request.method == 'POST':
		file = request.files['file']
		if not(request.form.has_key('apikey')):
			abort(403)
		elif not(app.config.has_key('API_KEY')) or app.config['API_KEY'] == 'fillSomethingInHere':
			return '<!doctype html>Set an API Key'
		elif request.form['apikey'] != app.config['API_KEY']:
			abort(403)
		if file:
			u = upload()
			u.save(file)
			return redirect(url_for('file_hash',filename=file.filename))
		else:
			abort(500)
	else:
		return send_from_directory(app.static_folder, 'upload.html')	

@app.route('/filehash/<filename>')
def file_hash(filename):
	u = upload()
	hash = u.get_hash(filename)
	return json_as_configured({'name':filename,'hash':hash})

@app.route('/file/<filename>')
def get_uploaded_file(filename):
	u = upload()
	return u.get_file(filename)	
