from flask import Blueprint, jsonify, request, abort
from src.settings import conn

conn.set_session(autocommit=True)

bp = Blueprint('payments', __name__, url_prefix='/payments')
REQUIRED_KEY_FOR_PAYMENTS = ['card_number', 'expiration_date', 'address_id']


@bp.route('', methods=['POST'])
def add():
    if any(key not in request.json for key in REQUIRED_KEY_FOR_PAYMENTS):
        return abort(400)
    card_number = request.json['card_number']
    expiration_date = request.json['expiration_date']
    address_id = request.json['address_id']

    cur = conn.cursor()

    try:
        cur.execute(
            """
            INSERT INTO payments(card_number, expiration_date, address_id)
                VALUES (%s, %s, %s)
                RETURNING id;
        """, (card_number, expiration_date, address_id))
    except Exception:
        return jsonify({'message': 'Something Went Wrong'})

    payment_id = cur.fetchall()[-1][-1]

    if 'user_id' in request.json:
        user_id = request.json.get('user_id')
        cur.execute(
        """
        INSERT INTO users_payments(payment_id, user_id)
            VALUES(%s, %s);
            """, (payment_id, user_id))
        
        return jsonify({'user_id': user_id, 'payment_id': payment_id})
    else:
        return jsonify({'payment_id': payment_id})