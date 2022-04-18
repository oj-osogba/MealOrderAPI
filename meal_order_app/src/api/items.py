from flask import Blueprint, jsonify, request, abort
from src.settings import conn

conn.set_session(autocommit=True)

bp = Blueprint('items', __name__, url_prefix='/items')
REQUIRED_KEY_FOR_ITEMS = ['name', 'category', 'quantity_avail', 'image', 'price']

@bp.route('', methods=['GET'])
def index():
    cur = conn.cursor()
    cur.execute("""
        SELECT * FROM items;
    """)
    item_records = cur.fetchall()

    return jsonify(serialize_item_records(item_records))



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
    except Exception:
        return jsonify(False)

    return jsonify(True)

def serialize_item_records(records):
    serialized_items = []
    for record in records:
        serialized_items.append({
            'id': record[0],
            'name': record[1],
            'category': record[2],
            'quantity': record[3],
            'price': str(record[4]),
            'image': record[5],
        })

    return serialized_items
