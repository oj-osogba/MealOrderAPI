from flask import Blueprint, jsonify, request, abort
from src.settings import conn

# Connect to your postgres DB
conn.set_session(autocommit=True)

bp = Blueprint('orders', __name__, url_prefix='/orders')

REQUIRED_KEY_FOR_ORDERS = ['payment_id', 'items']


@bp.route('', methods=['GET'])
def index():
    # Open a cursor to perform database operations
    cur = conn.cursor()
    cur.execute(
        """
        SELECT DISTINCT id FROM orders;
    """)

    order_ids = cur.fetchall()
    final_ls = []
    for order_id in order_ids:
        order_id = order_id[-1]
        cur.execute(
            """
            SELECT i.name, i.price, quantity FROM orders_items oi
                JOIN items i ON oi.item_id = i.id
                WHERE order_id = %s;
        """, (order_id, ))

        records = cur.fetchall()

        int_ls = []
        for record in records:
            int_ls.append({
                'id': order_id,
                'name': record[0],
                'price': str(record[1]),
                'quantity': record[2]
            })
        final_ls.append(int_ls)

    return jsonify(final_ls)


@bp.route('', methods=['POST', 'PUT', 'PATCH'])
def create():
    if any(key not in request.json for key in REQUIRED_KEY_FOR_ORDERS):
        return jsonify({'message': 'Insufficient Data'})

    name_id = request.json.get('name_id')
    contact_id = request.json.get('contact_id')
    address_id = request.json.get('address_id')
    payment_id = request.json['payment_id']
    items = request.json['items']
    user_id = request.json.get('user_id')
    cur = conn.cursor()
    
    if user_id is not None:
        cur.execute("""
            SELECT name_id, address_id, contact_id FROM users
                WHERE id = %s;
        """, (user_id,))

        ids = cur.fetchall()
        if len(ids) == 0:
            return jsonify({'message': 'User does not exist'})
        user_name_id = ids[-1][0]
        user_address_id = ids[-1][1]
        user_contact_id = ids[-1][2]

        if address_id is None and user_address_id:
            address_id = user_address_id
        
        if contact_id is None and user_contact_id:
            contact_id = user_contact_id
    
        if name_id is None:
            name_id = user_name_id
    
    if name_id is None:
        return jsonify({'message': 'Name on Order is required'})

    if address_id is None:
        return jsonify({'message': 'Address on Order is required'})

    if contact_id is None:
        return jsonify({'message': 'Contact info on Order is required'})


    valid = validate_item_list(items)

    if not valid:
        return jsonify({'message': 'Invalid Items'})

    items_available = validate_stock(items)

    if not items_available:
        return jsonify({'message': 'Order too large'})

    cur.execute(
        """
        INSERT INTO orders(name_id, contact_id, address_id, payment_id, user_id)
        VALUES(%s, %s, %s, %s, %s)
        RETURNING id;
    """, (name_id, contact_id, address_id, payment_id, user_id))
    order_id = cur.fetchall()[-1][-1]

    for item in items:
        item_id = item['item_id']
        quantity = item['quantity']
        cur.execute(
            """
               UPDATE items
                 SET quantity_avail = items.quantity_avail - %s
                 WHERE id = %s;  
            """, (quantity, item_id))
        cur.execute(
            """
                INSERT INTO orders_items(order_id, item_id, quantity)
                    VALUES(%s, %s, %s);
            """, (order_id, item_id, quantity))
        
    return jsonify({'order_id': order_id})


@bp.route('/<int:id>', methods=['GET'])
def view_order(id):
    cur = conn.cursor()

    cur.execute(
        """
        SELECT i.name, i.price, quantity FROM orders_items oi
            JOIN items i ON oi.item_id = i.id
            WHERE order_id = %s;
    """, (id, ))

    records = cur.fetchall()

    final_ls = []
    for record in records:
        final_ls.append({
            'name': record[0],
            'price': str(record[1]),
            'quantity': record[2]
        })
    return jsonify(final_ls)


def validate_item_list(items):
    for item in items:
        if 'item_id' not in item or 'quantity' not in item:
            return jsonify(False)
    return jsonify(True)

def validate_stock(items):
    cur = conn.cursor()
    for item in items:
        item_id = item['item_id']
        quantity = item['quantity']
        cur.execute("""
            SELECT quantity_avail FROM items
                WHERE id = %s; 
        """, (item_id, ))
        quantity_available = cur.fetchall()[-1][-1]
        if quantity_available - quantity < 0:
            return False
    return True




