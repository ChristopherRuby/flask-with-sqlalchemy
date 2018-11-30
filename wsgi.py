import os
import logging

from flask import Flask, request, render_template

from config import Config
app = Flask(__name__)
app.config.from_object(Config)


from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow # Order is important here!
db = SQLAlchemy(app)
ma = Marshmallow(app)

from models import Product
from schemas import products_schema, product_schema

import pdb;

@app.route('/hello')
def hello():
    return "Hello World!"

@app.route('/products')
def products():
    products = db.session.query(Product).all() # SQLAlchemy request => 'SELECT * FROM products'

    return render_template('home.html', products=products)

@app.route('/products/<int:id>')
def read_product(id):
    product = db.session.query(Product).get(id) # SQLAlchemy request => 'SELECT * FROM products'

    return render_template('product.html', product=product)


@app.route('/product', methods=['POST'])
def create_product():
    #pdb.set_trace()
    data = request.get_json()
    name = data['name']
    description = data.get('description')

    objProduct = Product()
    objProduct.name = name
    objProduct.description = description
    db.session.add(objProduct)
    db.session.commit()

    return ''
    #return product_schema.jsonify(product)
