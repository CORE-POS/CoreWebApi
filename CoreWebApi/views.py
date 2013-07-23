from flask import send_from_directory
from CoreWebApi import app
from CoreWebApi.database import db_session
from CoreWebApi.models import ProductUser, Products
from CoreWebApi.json_out import json_as_configured
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
