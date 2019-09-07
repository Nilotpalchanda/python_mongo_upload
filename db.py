from flask_pymongo import PyMongo
import urllib.parse
import server as s

s.app.config['MONGO_DBNAME'] = 'python_api'
s.app.config['MONGO_URI'] = 'mongodb://test:' + urllib.parse.quote_plus("test123") + '@ds219078.mlab.com:19078/python_api?retryWrites=false'
mongo = PyMongo(s.app)
