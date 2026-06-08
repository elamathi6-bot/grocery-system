from flask import Blueprint, render_template
from flask_login import login_required
from app import db
from app.models import Order, OrderItem, Product
from sqlalchemy import func

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@dashboard_bp.route('/')
@login_required
def index():
    total_products = Product.query.count()
    low_stock = Product.query.filter(Product.stock_quantity < 10).count()
    total_orders = Order.query.count()
    total_revenue = db.session.query(func.sum(Order.total_amount)).scalar() or 0

    top_products = db.session.query(
        Product.name,
        func.sum(OrderItem.quantity).label('total_sold')
    ).join(OrderItem).group_by(Product.name).order_by(func.sum(OrderItem.quantity).desc()).limit(5).all()

    recent_orders = Order.query.order_by(Order.order_date.desc()).limit(5).all()

    low_stock_products = Product.query.filter(Product.stock_quantity < 10).all()

    return render_template('dashboard.html',
        total_products=total_products,
        low_stock=low_stock,
        total_orders=total_orders,
        total_revenue=total_revenue,
        top_products=top_products,
        recent_orders=recent_orders,
        low_stock_products=low_stock_products
    )
