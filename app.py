from flask import Flask, jsonify, request
from flask_restful import Api,  Resource
from flask_swagger_ui import get_swaggerui_blueprint
import json
#from flask_restful_swagger_3 import swagger

app = Flask(__name__)
api = Api(app)

# Sample initial grocery list
grocery_list = [{'id': 1, 'item': 'Apples'},
                {'id': 2, 'item': 'Bananas'}]
next_id = 3


# Get all items
@app.route('/grocery', methods=['GET'])
def get_grocery_list():
    return jsonify(grocery_list)

# Add a new item
@app.route('/grocery', methods=['POST'])
def add_item():
    global next_id
    data = request.get_json()
    new_item = {'id': next_id, 'item': data['item']}
    grocery_list.append(new_item)
    next_id += 1
    return jsonify({'message': 'Item added successfully', 'item': new_item}), 201


# Update an existing item
@app.route('/grocery/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    data = request.get_json()
    for item in grocery_list:
        if item['id'] == item_id:
            item['item'] = data['item']
            return jsonify({'message': 'Item updated successfully', 'item': item})
    return jsonify({'message': 'Item not found'}), 404


# Delete an item
@app.route('/grocery/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    global grocery_list
    grocery_list = [item for item in grocery_list if item['id'] != item_id]
    return jsonify({'message': 'Item deleted successfully'})

# Register Swagger documentation
#swagger.register(app, api, api_spec_url='/api/swagger')

#if __name__ == '__main__':
#    app.run(debug=True)

# Add resource to API
api.add_resource(GroceryList, '/grocery')

# Register Swagger documentation
swagger.init_app(app)


SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': "Grocery App"}
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

@app.route('/static/swagger.json')
def swagger():
    with open('swagger.json', 'r') as f:
        return jsonify(json.load(f))
    
if __name__ == '__main__':
    app.run(debug=True)