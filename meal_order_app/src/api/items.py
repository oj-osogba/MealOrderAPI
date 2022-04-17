from flask import Blueprint, jsonify, request, abort
from src.settings import conn

conn.set_session(autocommit=True)

bp = Blueprint('items', __name__, url_prefix='/items')
REQUIRED_KEY_FOR_ITEMS = ['name', 'category', 'quantity_avail', 'image', 'price']


@bp.route('', methods=['POST', 'PUT', 'PATCH'])
def add():
    if any(key not in request.json for key in REQUIRED_KEY_FOR_ITEMS):
        return abort(400)
    name = request.json['name']
    category = request.json['category']
    quantity_avail = request.json['quantity_avail']
    image = request.json['image']
    price = request.json['price']

    cur = conn.cursor()

    try:
        cur.execute(
            """
            INSERT INTO items(name, category, quantity_avail, price, image)
            VALUES(%s, %s, %s, %s, %s)
            ON CONFLICT (name) DO UPDATE
                SET category = %s,
                    quantity_avail = items.quantity_avail + %s,
                    price = %s,
                    image = %s;
            """, (name, category, quantity_avail, price, image, category, quantity_avail, price, image)
        )
    except Exception as e:
        print(e)
        return jsonify(False)

    return jsonify(True)
