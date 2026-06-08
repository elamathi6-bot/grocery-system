from flask import Blueprint, request, jsonify, render_template
from app import db
from app.models import Order, OrderItem, Product

orders_bp = Blueprint('orders', __name__, url_prefix='/orders')

@orders_bp.route('/')
def index():
    orders = Order.query.order_by(Order.order_date.desc()).all()
    return render_template('orders.html', orders=orders)

@orders_bp.route('/api/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    order = Order(customer_name=data['customer_name'])
    db.session.add(order)

    total = 0
    for item in data['items']:
        product = Product.query.get(item['product_id'])
        if not product or product.stock_quantity < item['quantity']:
            return jsonify({'error': 'Insufficient stock'}), 400

        order_item = OrderItem(
            order=order,
            product_id=item['product_id'],
            quantity=item['quantity'],
            unit_price=product.price
        )
        product.stock_quantity -= item['quantity']
        total += float(product.price) * item['quantity']
        db.session.add(order_item)

    order.total_amount = total
    db.session.commit()
    return jsonify({'order_id': order.id, 'total': total}), 201

@orders_bp.route('/api/orders/<int:id>/status', methods=['PATCH'])
def update_status(id):
    order = Order.query.get_or_404(id)
    data = request.get_json()
    order.status = data['status']
    db.session.commit()
    return jsonify({'message': 'Status updated'})
