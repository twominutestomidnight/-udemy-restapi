from flask_restful import  Resource, reqparse
from flask_jwt import jwt_required
import sqlite3
from flask import jsonify


class Item(Resource):
    #@jwt_required()
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be blank!"
                        )
    #data = request.get_json()
    #data = parser.parse_args()

    @jwt_required()
    def get(self, name):
        item = self.find_by_name(name)
        if item:
            return item
        return {
            'message' : 'item not found'
        } , 404


    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "select * from items where name = ?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            return {
                'item': {
                    'name': row[0],
                    'price': row[1]
                }
            }

        return {
                   'message': 'item not found'
               }, 404

    @jwt_required()
    def post(self, name):
        if self.find_by_name(name):
            return {
                'message' : "An item with name '{}' already exists.".format(name)
            }, 400

        data = Item.parser.parse_args()
        item = {'name' : name, 'price': data['price']}

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "insert into items values (?,?)"
        result = cursor.execute(query, (item['name'], item['price'], ))

        connection.commit()
        connection.close()

        return item, 201


    def delete(self,name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message' : 'Item deleted'}

    @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()

        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            item = {'name' : name,
                    'price' : data['price']
                    }
            items.append(item)
        else:
            item.update(data)
        return item

class ItemList(Resource):
    @jwt_required()
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "select * from items"
        result = cursor.execute(query)
        #return {'items' : items}
        return jsonify(result)