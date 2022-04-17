from flask import Blueprint, jsonify, request, abort
from src.settings import conn

conn.set_session(autocommit=True)

bp = Blueprint('addresses', __name__, url_prefix='/address')
REQUIRED_KEY_FOR_ADDRESS = ['address_line_1', 'state', 'city', 'zip_code']


@bp.route('', methods=['POST', 'PUT', 'PATCH'])
def add():
    address_line_1 = request.json.get('address_line_1')
    state = request.json.get('state')
    city = request.json.get('city')
    zip_code = request.json.get('zip_code')
    address_line_2 = request.json.get('address_line_2')
    address_dict = {
        'address_line_1': address_line_1,
        'address_line_2': address_line_2,
        'city': city,
        'state': state,
        'zip_code': zip_code
    }

    cur = conn.cursor()

    if 'user_id' in request.json:
        user_id = request.json.get('user_id')
        cur.execute("""
            SELECT address_id FROM users
                WHERE id = %s;
        """, (user_id, ))
        address_ids = cur.fetchall()
        if len(address_ids) != 1:
            return jsonify({'message': 'User does not exist'})
        address_id = address_ids[-1][-1]
        if address_id:
            for variable in address_dict:
                if address_dict[variable] is not None:
                    if variable == 'address_line_1':
                        cur.execute(
                        """
                        UPDATE addresses
                            SET address_line_1 = %s
                            WHERE id = %s;
                            """, (address_dict[variable], address_id))
                    elif variable == 'address_line_2':
                        cur.execute(
                        """
                        UPDATE addresses
                            SET address_line_2 = %s
                            WHERE id = %s;
                            """, (address_dict[variable], address_id))
                    elif variable == 'city':
                        cur.execute(
                        """
                        UPDATE addresses
                            SET city = %s
                            WHERE id = %s;
                            """, (address_dict[variable], address_id))
                    elif variable == 'state':
                        cur.execute(
                        """
                        UPDATE addresses
                            SET state = %s
                            WHERE id = %s;
                            """, (address_dict[variable], address_id))
                    elif variable == 'zip_code':
                        cur.execute(
                        """
                        UPDATE addresses
                            SET zip_code = %s
                            WHERE id = %s;
                            """, (address_dict[variable], address_id))
                
            return jsonify(True)
        else:
            if any(key not in request.json for key in REQUIRED_KEY_FOR_ADDRESS):
                return jsonify({'message': 'Insufficient data'})

            cur.execute(
            """
            INSERT INTO addresses(address_line_1, state, city, zip_code, address_line_2)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id;
                """, (address_line_1, state, city, zip_code, address_line_2))

        address_id = cur.fetchall()[-1][-1]
        cur.execute("""
        UPDATE users
            SET address_id = %s
            WHERE id = %s;
        """, (address_id, user_id))
        return jsonify({'address_id': address_id})
    else:
        if any(key not in request.json for key in REQUIRED_KEY_FOR_ADDRESS):
            return jsonify({'message': 'Insufficient data'})

        cur.execute(
        """
        INSERT INTO addresses(address_line_1, state, city, zip_code, address_line_2)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id;
            """, (address_line_1, state, city, zip_code, address_line_2))

        address_id = cur.fetchall()[-1][-1]
        return jsonify({'address_id': address_id})
