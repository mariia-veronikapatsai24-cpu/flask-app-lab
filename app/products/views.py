from flask import Blueprint, render_template

products_bp = Blueprint('products', __name__, template_folder='templates')

@products_bp.route('/products')
def product_list():
    products = [
        {'name': 'Ноутбук', 'price': 25000},
        {'name': 'Смартфон', 'price': 12000},
        {'name': 'Навушники', 'price': 3000},
    ]
    return render_template('products/products.html', products=products)