from CoreWebApi import app
from flask import json, jsonify

def json_as_configured(dict):
	if type(dict) == type([]):
		dict = { 'results' : dict }
	if app.config.has_key('JSON_HEADERS') and app.config['JSON_HEADERS']:
		return jsonify(dict)
	else:
		return json.dumps(dict)
