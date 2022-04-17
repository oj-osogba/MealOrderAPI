from flask import Blueprint, jsonify, request, abort
from src.settings import conn
import secrets
import hashlib

# Connect to your postgres DB
conn.set_session(autocommit=True)

# Open a cursor to perform database operations
cur = conn.cursor()

bp = Blueprint('users', __name__, url_prefix='/users')
REQUIRED_KEY_FOR_USER = [
    'email_address', 'password', 'first_name', 'last_name'
]

REQUIRED_KEY_FOR_ADDRESS = ['address_line_1', 'state', 'city', 'zip_code']

REQUIRED_KEY_FOR_PAYMENTS = ['card_number', 'expiration_date', 'address_id']


@bp.route('', methods=['GET'])
def index():
    # Open a cursor to perform database operations
    cur = conn.cursor()
    cur.execute("""
        SELECT * FROM users;
    """)
    user_records = cur.fetchall()
    result = serialize_user_records(user_records)
    return jsonify(result)


@bp.route('/<int:id>', methods=['GET'])
def get_user(id: int):
    cur = conn.cursor()
    cur.execute(
        """
        SELECT name_id, address_id, contact_id, nutritional_rqt_id FROM users
        WHERE id = %s;
    """, (id, ))
    user_records = cur.fetchall()
    name_id, address_id, contact_id, nutritional_rqt_id = user_records[-1]
    cur.execute(
        """
        SELECT payment_id from users_payments
        WHERE user_id = %s;
    """, (id, ))

    payment_ids = [record[-1] for record in cur.fetchall()]

    cur.execute(
        """
        SELECT DISTINCT id FROM orders
            WHERE user_id = %s
            """, (id, ))

    order_ids = [record[-1] for record in cur.fetchall()]

    return jsonify({
        'name_id': name_id,
        'address_id': address_id,
        'payment_id': payment_ids,
        'order_id': order_ids,
        'nutritional_rqt_id': nutritional_rqt_id,
        'contact_id': contact_id,
        
    })


@bp.route('', methods=['POST'])
def create():
    # Open a cursor to perform database operations
    if any(key not in request.json for key in REQUIRED_KEY_FOR_USER):
        return abort(400)
    first_name = request.json.get('first_name')
    last_name = request.json.get('last_name')
    email_address = request.json.get('email_address')
    password = request.json.get('password')
    valid_password = validate_password(password)

    if not valid_password:
        return abort(400)
    cur = conn.cursor()
    cur.execute("""SELECT c.email_address FROM users u
                        JOIN contacts c ON u.contact_id = c.id
    """)
    email_list_records = [item[-1] for item in cur.fetchall()]
    if email_address in email_list_records:
        return abort(400)

    password = scramble(password)
    cur.execute(
        """
        INSERT INTO names(first_name, last_name)
            VALUES(%s, %s)
            RETURNING id;
    """, (first_name, last_name))
    name_id = cur.fetchall()[-1][-1]

    cur.execute(
        """
        INSERT INTO contacts(email_address)
            VALUES(%s)
            RETURNING id;
    """, (email_address, ))
    contact_id = cur.fetchall()[-1][-1]

    cur.execute(
        """
        INSERT INTO users(password, name_id, contact_id)
            VALUES(%s, %s, %s)
            RETURNING id;
    """, (password, name_id, contact_id))
    new_user_id = cur.fetchall()[-1][-1]

    return jsonify({'id': new_user_id, 'first_name': first_name})


# @bp.route('/<int:id>/update_address', methods=['PUT', 'PATCH'])
# def update_address(id):
#     if any(key not in request.json for key in REQUIRED_KEY_FOR_ADDRESS):
#         return abort(400)
#     address_line_1 = request.json['address_line_1']
#     state = request.json['state']
#     city = request.json['city']
#     zip_code = request.json['zip_code']
#     address_line_2 = request.json.get('address_line_2')

#     cur = conn.cursor()

#     cur.execute(
#         """
#         INSERT INTO addresses(address_line_1, state, city, zip_code, address_line_2)
#             VALUES (%s, %s, %s, %s, %s)
#             RETURNING id;
#     """, (address_line_1, state, city, zip_code, address_line_2))

#     address_id = cur.fetchall()[-1][-1]

#     cur.execute(
#         """
#         UPDATE users
#             SET address_id = %s
#             WHERE id = %s;
#     """, (address_id, id))

#     return jsonify({'address_id': address_id})


# @bp.route('/<int:id>/add_payment', methods=['POST'])
# def add_payment(id):
#     if any(key not in request.json for key in REQUIRED_KEY_FOR_PAYMENTS):
#         return abort(400)
#     card_number = request.json['card_number']
#     expiration_date = request.json['expiration_date']
#     address_id = request.json['address_id']

#     cur.execute(
#         """
#         INSERT INTO payments(card_number, expiration_date, address_id)
#             VALUES (%s, %s, %s)
#             RETURNING id;
#     """, (card_number, expiration_date, address_id))

#     payment_id = cur.fetchall()[-1][-1]

#     cur.execute(
#         """
#         INSERT INTO users_payments(payment_id, user_id)
#             VALUES(%s, %s);
#     """, (payment_id, id))

#     return jsonify({'payment_id': payment_id})


@bp.route('/<int:id>/orders', methods=['GET'])
def view_orders(id):
    cur = conn.cursor()

    order_keys = [
        'id', 'address_id', 'contact_id', 'name_id', 'payment_id', 'user_id',
        'delivered_at', 'created_at'
    ]
    cur.execute(
        """
        SELECT DISTINCT id, address_id, contact_id, name_id, payment_id, user_id, delivered_at, created_at FROM orders
        WHERE user_id = %s
    """, (id, ))

    order_records = cur.fetchall()

    serialized_dict = {}
    for record in order_records:
        for idx, key in enumerate(order_keys):
            serialized_dict[key] = record[idx]

    return jsonify(serialized_dict)


@bp.route('/<int:id>', methods=['DELETE'])
def delete_accout(id):
    cur = conn.cursor()

    try:
        cur.execute(
            """
            DELETE FROM users
                WHERE id = %s
        """, (id, ))
    except:
        return jsonify(False)
    return jsonify(True)


def serialize_user_records(records):
    cur = conn.cursor()

    serialized_records = {}
    for record in records:
        cur.execute("""
        SELECT payment_id FROM users_payments
            WHERE user_id = %s
                    """, (record[0],))
        payment_records = cur.fetchall()
        payments = [item[-1] for item in payment_records]
        cur.execute(
        """
        SELECT DISTINCT id FROM orders
            WHERE user_id = %s
            """, (record[0], ))
        order_records = cur.fetchall()
        orders = [item[-1] for item in order_records]

        serialized_records[str(record[0])] = {
            'name_id': record[2],
            'address_id': record[3],
            'payment_id': payments,
            'order_id': orders,
            'nutritional_rqt_id': record[4],
            'contact_id': record[5],
        }
    return serialized_records


def scramble(password: str):
    """Hash and salt the given password"""
    salt = secrets.token_hex(16)
    return hashlib.sha512((password + salt).encode('utf-8')).hexdigest()


def authenticate_credentials(username, password):
    valid = validate_username(username)
    if valid:
        valid = validate_password(password)
    return valid


def validate_username(username):
    if len(str(username)) < 3:
        return False
    return True


def validate_password(password):
    if len(str(password)) < 8:
        return False
    return True
