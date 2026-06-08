from flask import Blueprint, request, jsonify, render_template, Response
from flask_login import login_required
from app import db
from app.models import Product, Order, OrderItem
import csv
import io

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

@inventory_bp.route('/export/products')
@login_required
def export_products():
    products = Product.query.all()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['ID', 'Name', 'Category', 'Price', 'Stock', 'Created At'])
    for p in products:
        writer.writerow([p.id, p.name, p.category, p.price, p.stock_quantity, p.created_at])
    output.seek(0)
    return Response(output, mimetype='text/csv',
        headers={'Content-Disposition': 'attachment;filename=inventory.csv'})

@inventory_bp.route('/export/orders')
@login_required
def export_orders():
    orders = Order.query.all()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Order ID', 'Customer', 'Total', 'Status', 'Date'])
    for o in orders:
        writer.writerow([o.id, o.customer_name, o.total_amount, o.status, o.order_date])
    output.seek(0)
    return Response(output, mimetype='text/csv',
        headers={'Content-Disposition': 'attachment;filename=orders.csv'})
