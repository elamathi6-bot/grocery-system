from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required
from app import db
from app.models import Supplier, Product

suppliers_bp = Blueprint('suppliers', __name__, url_prefix='/suppliers')

@suppliers_bp.route('/')
@login_required
def index():
    suppliers = Supplier.query.all()
    return render_template('suppliers.html', suppliers=suppliers)

@suppliers_bp.route('/api/suppliers', methods=['POST'])
@login_required
def add_supplier():
    data = request.get_json()
    supplier = Supplier(
        name=data['name'],
        contact=data.get('contact'),
        email=data.get('email'),
        phone=data.get('phone'),
        address=data.get('address')
    )
    db.session.add(supplier)
    db.session.commit()
    return jsonify(supplier.to_dict()), 201

@suppliers_bp.route('/api/suppliers/<int:id>', methods=['DELETE'])
@login_required
def delete_supplier(id):
    supplier = Supplier.query.get_or_404(id)
    db.session.delete(supplier)
    db.session.commit()
    return jsonify({'message': 'Supplier deleted'})

@suppliers_bp.route('/api/suppliers/<int:id>/products', methods=['GET'])
@login_required
def get_supplier_products(id):
    supplier = Supplier.query.get_or_404(id)
    return jsonify([p.to_dict() for p in supplier.products])
