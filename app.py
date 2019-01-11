from flask import Flask
from flask_restful import  Api
from flask_jwt import JWT

from security import authenticate, identity
from user import UserRegister
from item import Item, ItemList


app = Flask(__name__)
app.secret_key = 'jose'
api = Api(app)

import datetime
jwt = JWT(app, authenticate, identity) # /auth
#app.config['JWT_EXPIRATION_DELTA'] = datetime.timedelta(seconds=20)


api.add_resource(Item,'/item/<string:name>') #http://127.0.0.1:5000/student/Rolf
api.add_resource(ItemList,'/items')
api.add_resource(UserRegister,'/register')

if __name__ == '__main__':
    app.run(port = 5000, debug = True)