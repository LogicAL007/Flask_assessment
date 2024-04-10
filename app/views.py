from flask import Blueprint, render_template, flash, redirect, request, jsonify
from app.models import Product, Cart, Order
from flask_login import login_required, current_user
from app import db


views = Blueprint('views', __name__)

@views.route('/')
def home_page():
    return "<p>This project was done by Team B in Data Epic</p>"


@views.route('/add-to-cart/<item_id>')
def add_to_cart(item_id):
    '''
    Adds a specified item to the user's cart or increases its quantity if it already exists in the cart.
    
    Parameters:
        item_id: The ID of the product to add to the cart.
    
    Returns:
        JSON response with a success message and HTTP status code 200 on successful addition or update, 
        or an error message with appropriate HTTP status code if the product doesn't exist, 
        or if there's an exception during database operation.'''
    test_user_id = 1  

    item_to_add = Product.query.get(item_id)
    if item_to_add:
        item_exists = Cart.query.filter_by(product_link=item_id, customer_link=test_user_id).first()
        if item_exists:
            try:
                item_exists.quantity += 1
                db.session.commit()
                return jsonify(message=f'Quantity of {item_exists.product.product_name} has been updated'), 200
            except Exception as e:
                return jsonify(error=str(e)), 500

        new_cart_item = Cart(quantity=1, product_link=item_id, customer_link=test_user_id)
        try:
            db.session.add(new_cart_item)
            db.session.commit()
            return jsonify(message=f'{item_to_add.product_name} added to cart'), 200
        except Exception as e:
            return jsonify(error=str(e)), 500
    else:
        return jsonify(error='Product not found'), 404



@views.route('/cart', methods=['GET', 'POST'])
# @login_required 
def show_cart():
    """
    Displays the current user's cart, including product names, quantities, and prices.
    
    Retrieves all cart items for the current user, calculates the subtotal for each item, and computes the total cart amount. Responds with this data in JSON format.
    
    Returns:
        JSON response containing the cart items' details and the total amount.
    """   
    test_user_id = 1 

    cart_items = Cart.query.filter_by(customer_link=test_user_id).all()
    cart_data = [{
        'product_name': item.product.product_name,
        'quantity': item.quantity,
        'price_per_item': item.product.current_price,
        'subtotal': item.quantity * int(item.product.current_price)
    } for item in cart_items]

    total_amount = sum(float(item['subtotal']) for item in cart_data) 
    return jsonify(cart=cart_data, total=total_amount)

@views.route('/pluscart')
# @login_required
def plus_cart():
    """
    Increases the quantity of a specific item in the user's cart by one.
    
    Parameters:
        cart_id (int): Query parameter specifying the cart item whose quantity is to be increased.
    
    Returns:
        JSON response with the updated quantity and new total cart amount if successful, 
        or an error message with appropriate HTTP status code if the cart item is not found, 
        no cart ID is provided, or the current user does not have permission to modify the cart item.
    """
    test_user_id = 1 

    cart_id = request.args.get('cart_id')
    if cart_id is None:
        return jsonify({'error': 'No cart ID provided'}), 400

    cart_item = Cart.query.get(cart_id)
    if not cart_item:
        return jsonify({'error': 'Cart item not found'}), 404

    # Check if the cart_item belongs to the test_user_id
    if cart_item.customer_link != test_user_id:
        return jsonify({'error': 'Access denied'}), 403

    cart_item.quantity += 1 
    db.session.commit()

    cart = Cart.query.filter_by(customer_link=test_user_id).all()

    amount = sum(int(item.product.current_price) * item.quantity for item in cart)

    data = {
        'quantity': cart_item.quantity,    
        'total': amount  
    }

    return jsonify(data)

@views.route('/minuscart', methods=['GET'])
# @login_required
def minus_cart():
    """
    Decreases the quantity of a specific item in the user's cart by one, if its quantity is greater than zero.
    
    Parameters:
        cart_id (int): Query parameter specifying the cart item whose quantity is to be decreased.
    
    Returns:
        JSON response with the updated quantity and new total cart amount if successful, 
        or an error message with appropriate HTTP status code if the cart item is not found or has quantity zero,
        no cart ID is provided, or the operation results in negative quantity.
    """   
    test_user_id = 1 

    cart_id = request.args.get('cart_id')
    if cart_id is None:
        return jsonify({'error': 'No cart ID provided'}), 400

    cart_item = Cart.query.get(cart_id)
    if not cart_item :
        return jsonify({'error': 'Cart item not found or access denied'}), 404

    if cart_item.quantity > 0:
        cart_item.quantity -= 1
        db.session.commit()

        cart = Cart.query.filter_by(customer_link=test_user_id).all()

        amount = sum(int(int(item.product.current_price) * item.quantity) for item in cart)
        
        data = {
            'quantity': cart_item.quantity,
            'amount': amount,
            'total': amount
        }

        return jsonify(data)
    else:
        return jsonify({'error': 'Quantity cannot be less than zero'}), 400


@views.route('/removecart', methods=['GET'])
# @login_required
def remove_cart():
    """
    Removes a specific item from the user's cart entirely, regardless of quantity.
    
    Parameters:
        cart_id (int): Query parameter specifying the cart item to be removed.
    
    Returns:
        JSON response indicating the quantity of the removed item and the new total cart amount if successful, 
        or an error message with appropriate HTTP status code if the cart item is not found,
        no cart ID is provided, or the current user does not have permission to remove the cart item.
    """
    test_user_id = 1
    cart_id = request.args.get('cart_id')
    if not cart_id:
        return jsonify({'error': 'No cart ID provided'}), 400

    cart_item = Cart.query.get(cart_id)
    if not cart_item:
        return jsonify({'error': 'Cart item not found'}), 404
    if cart_item.customer_link != test_user_id:
        return jsonify({'error': 'Access denied'}), 403
    quantity_deleted = cart_item.quantity 
    db.session.delete(cart_item)
    db.session.commit()
    cart = Cart.query.filter_by(customer_link=test_user_id).all()
    amount = sum(item.product.current_price * item.quantity for item in cart)

    data = {
        'quantity': quantity_deleted, 
        'amount': amount,              
        'total': amount               
    }

    return jsonify(data)
