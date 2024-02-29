from flask import Flask, jsonify, request
import json

app = Flask(__name__)

db_path = 'servers_db.json'

def read_db():
    with open(db_path, 'r') as f:
        return json.load(f)

def write_db(data):
    with open(db_path, 'w') as f:
        json.dump(data, f, indent=4)

@app.route('/addProduct', methods=['POST'])
def add_product():
    new_product = request.json
    db = read_db()
    db['products'].append(new_product)
    write_db(db)
    return jsonify(code=201, message="Product added"), 201

@app.route('/getProducts')
def get_products():
    products = read_db().get('products', [])
    return jsonify(code=200, products=products)

if __name__ == '__main__':
    app.run(port=3002)

