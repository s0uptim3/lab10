from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS # Import Cors
import json
import os



app = Flask(__name__)
CORS(app, origins='*', allow_headers='*', supports_credentials=False) #enable cors

def load_products():
    with open('products.json', 'r') as f:
        return json.load(f)['products']
    


@app.route('/products', methods=['GET'])
@app.route('/products/<int:product_id>', methods=['GET'])
def get_products(product_id=None):
    products = load_products()
    if product_id is None:
        return jsonify({"products": products})
    else:
        product = next((p for p in products if p['id'] == product_id), None)

        return jsonify(product) if product else ('', 404)
    
@app.route('/products/add', methods=['POST'])
def add_product():
    new_product = request.json
    products = load_products()
    new_product['id'] = len(products) + 1
    products.append(new_product)
    with open('products.json', 'w') as f:
        json.dump({"products": products}, f)
    return jsonify(new_product), 201

@app.route('/products/edit/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    products = load_products()
    for p in products:
        if p['id'] == product_id:
            updated_product = request.json
            p.update(updated_product)
            with open('products.json', 'w') as f:
                json.dump({"products": products}, f)
            return jsonify(p), 201
    return jsonify({"error": "Product not found"}, product_id)
    
@app.route('/products/<int:product_id>', methods=['DELETE'])
def remove_product(product_id):
    products = load_products()
    del_index = None
    for index, product in enumerate(products):
        if product['id'] == product_id:
            del_index = index
            break

    if del_index is not None:
        del products[del_index]

        with open('products.json', 'w') as f:
            json.dump({"products": products}, f)

        return jsonify({"message": f"Product with ID {product_id} has been removed"}), 200
    else:
        return jsonify({"error"}), 404


    


@app.route('/product-images/<path:filename>')
def get_image(filename):
    return send_from_directory('product-images', filename)

if __name__ == '__main__':
    app.run(debug=True)