from flask import Blueprint, jsonify, request, abort
from src.settings import conn

conn.set_session(autocommit=True)

bp = Blueprint('contacts', __name__, url_prefix='/contacts')
REQUIRED_KEY_FOR_CONTACTS = ['email_address']

@bp.route('', methods=['POST', 'PUT', 'PATCH'])
def add():
    cur = conn.cursor()

    email_address = request.json.get('email_address')
    phone_number = request.json.get('phone_number')
    user_id = request.json.get('user_id')

    contact_dict = {
        'email_address': email_address,
        'phone_number': phone_number
    }

    if user_id is None:
        if any(key not in request.json for key in REQUIRED_KEY_FOR_CONTACTS):
            return abort(400)
        try:
            cur.execute(
                """
                INSERT INTO contacts (email_address, phone_number)
                    VALUES(%s, %s)
                    RETURNING id;
                """, (email_address, phone_number))
        except Exception:
            return jsonify({'message': 'E-mail already exists'})
        
    else:
        cur.execute("""
            SELECT contact_id FROM users
                WHERE id = %s;
        """,(user_id, ))
        contact_ids = cur.fetchall()
        if len(contact_ids) == 0:
            return jsonify({'message': 'User does not Exist'})
        contact_id = contact_ids[-1][-1]
        for variable in contact_dict:
            if contact_dict[variable] is not None:
                if variable == 'email_address':
                    cur.execute(
                        """
                        UPDATE contacts
                            SET email_address = %s
                            WHERE id = %s;
                        """, (contact_dict[variable], contact_id))
                elif variable == 'phone_number':
                    cur.execute(
                        """
                        UPDATE contacts
                            SET phone_number = %s
                            WHERE id = %s;
                        """, (contact_dict[variable], contact_id))

        return jsonify(True)
        

