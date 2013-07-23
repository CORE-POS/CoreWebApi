from flask import Flask
app = Flask(__name__)
app.config.from_object('CoreWebApi.default_settings')

import CoreWebApi.views
