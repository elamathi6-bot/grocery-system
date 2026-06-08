from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required
from app import db
from app.models import Product

inventory_bp = Blueprint('inventory', __name__, url_prefix='/inventory')

@inventory_bp.route('/')
@login_required
def index():
    products = Product.query.all()
    categories = list(set([p.category for p in products if p.category]))
    return render_template('inventory.html', products=products, categories=categories)

@inventory_bp.route('/api/products', methods=['GET'])
@login_required
def get_products():
    products = Product.query.all()
    return jsonify([p.to_dict() for p in products])

@inventory_bp.route('/api/products', methods=['POST'])
@login_required
def add_product():
    data = request.get_json()
    product = Product(
        name=data['name'],
        category=data.get('category'),
        price=data['price'],
        stock_quantity=data.get('stock_quantity', 0)
    )
    db.session.add(product)
    db.session.commit()
    return jsonify(product.to_dict()), 201

@inventory_bp.route('/api/products/<int:id>', methods=['PUT'])
@login_required
def update_product(id):
    product = Product.query.get_or_404(id)
    data = request.get_json()
    product.name = data.get('name', product.name)
    product.price = data.get('price', product.price)
    product.stock_quantity = data.get('stock_quantity', product.stock_quantity)
    db.session.commit()
    return jsonify(product.to_dict())

@inventory_bp.route('/api/products/<int:id>', methods=['DELETE'])
@login_required
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Product deleted'})
