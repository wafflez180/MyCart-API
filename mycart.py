from flask import Flask, jsonify, request, abort
from flask.ext.pymongo import PyMongo
from bson import json_util
import json

app = Flask(__name__)
mongo = PyMongo(app)

app.debug = True

@app.route('/api/v1/products', methods=['GET'])
def get_products():
    products = list(mongo.db.products.find())
    return json.dumps(products, sort_keys=True, indent=4, default=json_util.default)

@app.route('/api/v1/products/<string:barcode>', methods=['GET'])
def get_product(barcode):
    product = mongo.db.products.find_one({'barcode' : barcode})
    if product is None:
	return jsonify({'error': 'Product not found'}), 404

    return json.dumps(product, sort_keys=True, indent=4, default=json_util.default)

@app.route('/api/v1/products/add', methods=['POST'])
def add_product():
    data = request.get_json()
    if not data or 'name' in data:
        abort(400)

    product = {
        'name': data['name'],
        'barcode': data['barcode'],
        'brand': data['brand'],
        'price': data['price']
    }
    mongo.db.products.insert(product)
    return jsonify({'product': product}), 201

if __name__ == "__main__":
    app.run(host='0.0.0.0')
