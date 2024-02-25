'''from flask import Flask, jsonify, request
from flask_restful import Api,  Resource
from flask_swagger_ui import get_swaggerui_blueprint
from werkzeug.urls import unquote
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
api.add_resource(grocery_list, '/grocery')

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
    app.run(debug=True)'''

from flask import Flask, jsonify, request
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)

# Sample data (in-memory database)
books = [
    {"id": 1, "title": "Book 1", "author": "Author 1"},
    {"id": 2, "title": "Book 2", "author": "Author 2"}
]
next_id = 3

# Get all books
@app.route('/books', methods=['GET'])
def get_books():
    """
    Retrieve all books.
    ---
    responses:
      200:
        description: A list of books
    """
    return jsonify(books)

# Add a new book
@app.route('/books', methods=['POST'])
def add_book():
    """
    Add a new book.
    ---
    parameters:
      - in: body
        name: book
        description: The book to add
        schema:
          type: object
          properties:
            title:
              type: string
              description: The title of the book
            author:
              type: string
              description: The author of the book
    responses:
      201:
        description: The newly added book
    """
    global next_id
    data = request.get_json()
    book = {"id": next_id, "title": data["title"], "author": data["author"]}
    books.append(book)
    next_id += 1
    return jsonify(book), 201

# Update a book
@app.route('/books/<int:id>', methods=['PUT'])
def update_book(id):
    """
    Update a book.
    ---
    parameters:
      - in: path
        name: id
        description: The ID of the book to update
        required: true
        type: integer
      - in: body
        name: book
        description: The updated book information
        schema:
          type: object
          properties:
            title:
              type: string
              description: The new title of the book
            author:
              type: string
              description: The new author of the book
    responses:
      200:
        description: The updated book
      404:
        description: Book not found
    """
    for book in books:
        if book["id"] == id:
            data = request.get_json()
            book["title"] = data["title"]
            book["author"] = data["author"]
            return jsonify(book)
    return jsonify({"error": "Book not found"}), 404

# Delete a book
@app.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    """
    Delete a book.
    ---
    parameters:
      - in: path
        name: id
        description: The ID of the book to delete
        required: true
        type: integer
    responses:
      204:
        description: Book deleted successfully
      404:
        description: Book not found
    """
    global books
    initial_length = len(books)
    books = [book for book in books if book["id"] != id]
    if len(books) < initial_length:
        return '', 204
    else:
        return jsonify({"error": "Book not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
