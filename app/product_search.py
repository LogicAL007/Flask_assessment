from flask import Blueprint, request, jsonify
from website.models import Product
from website import db

productsearch = Blueprint('productsearch', __name__)

@productsearch.route('/productsearch', methods=['GET', 'POST'])
def search_page():
    if request.method == 'POST':
        search_query = request.form.get('search')
        min_price = request.form.get('min_price')
        max_price = request.form.get('max_price')

        query = Product.query.filter(Product.product_name.ilike(f'%{search_query}%'))

        if min_price and max_price:
            query = query.filter(Product.current_price >= float(min_price), Product.current_price <= float(max_price))

        items = query.all()

        results = [
            {
                'id': item.id,
                'product_name': item.product_name,
                'price': item.current_price,
                'product_picture_link': item.product_picture,
                'stock_status': 'Out of Stock' if item.in_stock > 0 else 'In Stock'
            } for item in items
        ]

        return jsonify(results=results)

    items = Product.query.all()
    results = [
        {
            'id': item.id,
            'product_name': item.product_name,
            'price': item.current_price,
            'stock_status': 'In Stock' if item.in_stock > 0 else 'Out of Stock'
        } for item in items
    ]
    return jsonify(results=results)
